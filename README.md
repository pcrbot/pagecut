没有在LINUX中测试过  
安装依赖selenium  
在服务器中安装chrome浏览器和chromedriver，需要相同版本  
将14行的chromedriver改为你的chromedriver的路径  
45行C:\\nb2\\mimibot\\src\\plugins\\pcr-rank\\img\\imgs中的C:\\nb2\\mimibot\\src\\plugins\\pcr-rank\\img改为你RES_DIR的路径  
效果如图  
![图片](https://user-images.githubusercontent.com/81564864/134680689-859021d8-b0a0-4985-a930-1bb8f849aeb7.png)  
已知问题：会阻塞其他事件，当访问的链接加载较慢，会影响其他事件的相应  


