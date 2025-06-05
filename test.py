import os
import sys
from datetime import datetime
import requests
from lxml import etree
import logging
import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'D:\\Coding\\Code\\pj_learn_001\\Log\\sanctionslist\\sanctions_parser_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

def web_crawler():
    """
    Function to download the OFAC sanctions list from the US Treasury website.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    url = 'https://sanctionslistservice.ofac.treas.gov/api/PublicationPreview/exports/CONS_ENHANCED.XML'
    res = requests.get(url=url, headers=headers)
    if res.status_code == 200:
        with open(file_path, 'wb') as f:
            f.write(res.content)
        print("Download successful.")
    else:
        print("Failed to download the sanctions list.")
    print(res.status_code)


def parse_xml(input_file_path):

    """
    Parses the downloaded XML file and extracts relevant information.

    Args:
        input_file_path (str): Path to the XML file to be parsed.

    Returns:
        None
    """

    try:
        """使用 lxml 解析 OFAC XML 文件"""
        # 解析 XML 文件
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse(input_file_path, parser)
        root = tree.getroot()

        # 查看命名空间（自动检测）
        namespaces = {
            'default': root.nsmap[None] if None in root.nsmap else '',
            'xsi': root.nsmap.get('xsi', '')
        }
        logging.info(f"默认命名空间: {namespaces['default']}")
        sanctions = []
        # 使用 XPath 查询 entities 元素
        entities = root.xpath('//default:entities/default:entity', namespaces=namespaces)
        logging.info(f"found total {len(entities)} entity in raw file")
        for entity in entities:
            logging.info(f"No.{entities.index(entity) + 1}: entity ID: {entity.xpath('./@id', namespaces=namespaces)}")
            related_sanctions = {}
            # to find SanctionsProgram
            sanctions_program = entity.xpath('./default:sanctionsPrograms/default:sanctionsProgram/text()', namespaces=namespaces)
            if 'CMIC-EO13959' not in sanctions_program:
                continue  # 如果没有 'CMIC-EO13959'，直接跳过
            if len(sanctions_program) > 1:
                raise ValueError(f"Unexpected multiple values in sanctions_program: {sanctions_program}")
            sanctions_program = sanctions_program[0]

            # to find entity_names
            names = entity.xpath('./default:names/default:name', namespaces=namespaces)
            for name in names:
                is_primary = name.xpath('./default:isPrimary[text()="true"]', namespaces=namespaces)
                if is_primary:
                    translations = name.xpath('./default:translations/default:translation', namespaces=namespaces)
                    for translation in translations:
                        name_parts = translation.xpath('./default:nameParts/default:namePart', namespaces=namespaces)
                        if len(name_parts) != 1:
                            raise ValueError(f"Unexpected multiple nameParts in translation: {name_parts}")
                        value = translation.xpath('./default:nameParts/default:namePart/default:value/text()',
                                                  namespaces=namespaces)
                        entity_name = value[0] if value else None  # 转换为字符串，如果列表
                        logging.info(f'entity_name: {entity_name}')
                        logging.info(f'entity_name data type:{type(entity_name)}')

            related_sanctions['EntityName'] = entity_name
            related_sanctions['SanctionProgram'] = sanctions_program
            logging.info(f'related_sanctions: {related_sanctions}')

            # to find features
            features = entity.xpath('./default:features/default:feature', namespaces=namespaces)
            if features:
                logging.info(f"found total {len(features)} features in entity")
                related_identifiers = []
                for index, feature in enumerate(features):
                    logging.info(f'feature id: {feature.attrib["id"]}')
                    feature_type = feature.xpath('./default:type/text()', namespaces=namespaces)
                    feature_type = feature_type[0] if feature_type else None
                    feature_value = feature.xpath('./default:value/text()', namespaces=namespaces)
                    feature_value = feature_value[0] if feature_value else None
                    logging.info(f'feature_type: {feature_type}\n'
                                 f'feature_value: {feature_value}')

                    if feature_type == 'Equity Ticker':
                        related_identifiers.append(f'Ticker:{feature_value}')
                    elif feature_type == 'ISIN':
                        related_identifiers.append(f'ISIN:{feature_value}')
                    logging.info(f"related_identifiers: {related_identifiers}")
                    # sys.exit(-1)

                    if feature_type == 'Effective Date (CMIC)':
                        related_sanctions['EffectiveDate'] = feature_value
                    elif feature_type == 'Purchase/Sales For Divestment Date (CMIC)':
                        related_sanctions['DivestmentDate'] = feature_value
                    elif feature_type == 'Listing Date (CMIC)':
                        related_sanctions['SanctionListingDate'] = feature_value

                related_sanctions['identifiers'] = related_identifiers
                logging.info("related_sanctions: {related_sanctions}")
                sanctions.append(related_sanctions)

        sanction_df = pd.DataFrame(sanctions)
        sanction_df = sanction_df.explode('identifier', ignore_index=True)
        sanction_df['identifiers'] = sanction_df['identifiers'], sanction_df['identifiers'] = sanction_df['identifiers'].str.split(':').str[0], sanction_df['identifiers'].str.split(':').str[1]
        df = sanction_df[sanction_df['identifier'].isna()]
        logging.info(df.shape)

        sanction_df['identifier'] = sanction_df[['identifier', 'IdentifierType']].apply(lambda x: identify_format(x[0], x[1]), axis=1)
        sanction_df['identifier'] = sanction_df['identifier'].str.replace('300114-CN', '302132-CN')
        sanction_df['FileDate'] = today
        sanction_df = sanction_df[['FileDate', 'EntityName', 'SanctionProgram', 'SanctionListingDate', 'DivestmentDate', 'EffectiveDate', 'Identifier', 'IdentifierType']]
        sanction_df.to_csv(csv_path, index=False)

    except Exception as e:
        logging.error(f"解析XML文件时发生错误: {str(e)}")
        raise


def identify_format(identifier, identifier_type):
    if identifier_type == 'Ticker':
        t = identifier.strip()[:-2]
        region = identifier.strip()[-2:]
        if region == 'HK':
            t = t.lstrip('0')

            return '-'.join([t.strip(), region.strip()])
        else:
            return identifier


if __name__ == '__main__':
    today = datetime.now().strftime('%Y-%m-%d')
    current_date = datetime.now().strftime('%Y%m%d')
    order_date= current_date
    file_dir = 'D:\\Coding\\Code\\pj_learn_001\\DataFile\\sanctionslist'
    file_dir_date = f'D:\\Coding\\Code\\pj_learn_001\\DataFile\\sanctionslist\\{order_date}'
    file_path = f'{file_dir_date}\\us_sanctions_list.xml'
    csv_path = f'{file_dir_date}\\us_sanctions_list.csv'
    os.makedirs(file_dir_date, exist_ok=True)
    logging.info(f"11111111111111")
    web_crawler()
    logging.info(f"222222222222222")
    parse_xml(file_path)
    logging.info(f"333333333333333333")


