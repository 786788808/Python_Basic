第一次留意到`requirement.txt`还是在看别人code的时候发现的，mark down一下...  
进到自己的虚拟环境中   
![image](https://user-images.githubusercontent.com/32427537/210240586-e9e2435c-2934-4935-ae5a-f72da7662976.png)
![image](https://user-images.githubusercontent.com/32427537/210240785-003e2cfb-a3f7-4eea-8f64-792ef7c77f2f.png)  
执行安装  
`pip install pipreqs`  
`pipreqs . --encoding=utf8--force`  
![image](https://user-images.githubusercontent.com/32427537/210240987-a5d4bf4c-2a23-4e3a-9b11-7c8d3b7f9e6d.png)  
![image](https://user-images.githubusercontent.com/32427537/210241607-4ad88588-fce7-4cd7-8517-398bcb22e98b.png)  
可以看到`requirement.txt`出来了   
![image](https://user-images.githubusercontent.com/32427537/210243376-7d17cf7b-1652-4fe9-bcf3-4ec66b9e27fe.png)
![image](https://user-images.githubusercontent.com/32427537/210241746-e23ea2f9-441e-4b00-950d-aeb896cbb7d9.png)    
![image](https://user-images.githubusercontent.com/32427537/210245924-78496bbb-a844-4902-9b82-54df1801bbde.png)

环境项目导入：`pip install -r requirements.txt`  

还有一个命令，可以google一下他们的区别。  
`pip freeze > requirements.txt` or `pip freeze > E:\xxx\requirements.txt`(指定一个路劲，不指定的话就直接生成到当前路径下)  
pipreqs 是一个第三方库，只生成当前项目中所用到的依赖包及其版本号，而pip freeze 方式会把所有包全部列出并生成（不过如果你进到了有虚拟环境，那就可以只生成当前项目de)  
参考资料：[pipreqs](https://github.com/bndr/pipreqs)    

