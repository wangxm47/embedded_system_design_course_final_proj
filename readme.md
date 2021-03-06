# 嵌入式系统设计期末项目

## 项目基本结构( 还未完全确定 )

进展：https://docs.qq.com/doc/DWWpPYVJZQWJOZkFi


## 需求


## 基本效果

stc 单片机上有以下5个状态

- 等待密码输入
    
    - 出现当前时间(hh-mm-ss)的时候为等待输入状态

- 密码输入正确

    - 7段管出现`tttttttt`代表输入正确

- 密码输入错误

    - 7段管出现`ffffffff`代表输入错误

- 开门: 

    - 出于开门状态的时候，p47 LED 灯出于点亮状态
    
- 报警

    - 当门出于打开状态 `一定时间` 之后，会进入报警状态，此时 P46,P47 LED灯都处于报警状态

单片机按键：

// keycode 和 键盘按键之间的对应
// 27 => A, 28 => B, 29 => C, 30 => D
#define CLOSE_DOOR_KEY_CODE 30 
#define OPEN_DOOR_KEY_CODE 29
#define REINPUT_KEY_CODE 28
#define INPUT_CONFIRM_KEY_CODE 27

## 连线方式

### 51 单片机连接 esp8266 模块

这两个模块之间需要通过 urat 来传输信息

- 开门的指令

- 当前门的状态

- 在门输入的密码

具体连线如下

- esp8266 G(gound) <=> 51 GND 

- esp8266 Tx(transfer) <=> 51 P16(相当于 UART RX)

- esp8266 Rx(receive) <=> 51 P17(相当于 UART TX)

### 使用串口助手调试单片机

通过 两头USB 的线，连接电脑和单片机, 之后再把烧板的接口和UART接口连接起来，实现通过烧写接口向单片机UART串口发送/从单片机接收

具体连线如下:

- P30 <=> P17

- P31 <=> p16

## 信息传递约定

### 单片机 => wifi 模块

- `八位数字(0 - 9)`: 代表密码

- `cccccccc`：当前门的状态是关闭

- `oooooooo`：当前门的状态是开启

### wifi 模块 => 单片机

- `t`: 密码正确

- `f`: 密码错误

- `o`: 直接开门

### wifi 模块和后台服务器之间


### 数据库部分

处于轻量化考虑使用的是功能简单的数据库`Tinydb`，这是一个极为轻量化的 `nosql` 类型数据库 

使用数据库来存储被访问的密码输入的记录以及门锁报警记录

{
    事件:(1 -> 密码输入), (2 -> 报警)
    结果:(1 -> 密码输入结果)，(报警原因)
    时间:(事件发生时间)
}


## API design

// todo 
- GET /poll : 轮询当前门锁的状态
    
    - request: 没有参数

    - reponse: 门的状态【开启或者关闭】

- POST: /open-door : 发送开门请求到服务器
    
    - request: 
        - string: password

    - response:
        
        - string: result(true => 密码正确 / false => 密码错误)


- GET: / : 获取本地数据库的状态，管理者页面
    
    - request: 

    - response : 

        - log