# SSAB ( Smart Shopping Assistance bot )

## 목차
*  📝 [개요](#-개요)
*  🛠 [기술 및 도구](#-기술-및-도구)
*  ✨ [기능 구현](#-기능-구현)
*  ⏰ [일정](#-일정)

## **📝 개요**
> **프로젝트** : 쇼핑 도우미
>
> **인원** : 4인
> |팀장|팀원|팀원|팀원|
> |:--|:--|:--|:--|
> |표홍운|채승훈|김덕영|김혁제|
> 
> **주제** : 무인 이동체를 이용해서 특정 위치에서 원하는 물품을 Cam을 통해 인식하여 물품을 받고 사용자에게 전달하기.
> 
> **제작 기간** : 6.30 ~ 7.24
> 
> **주요 기능**   
> > * 받아야 하는 물품의 위치로 Mobile이동체 이동   
> > * Cam을 활용하여 Mobile 이동체의 인식및 물품 수량 배출   
> > * 받은 물품을 대기 위치로 이동   



## **🛠 기술 및 도구**   
> **언어** : <img alt="python" src ="https://img.shields.io/badge/python-3776AB.svg?&style=flat-square&logo=python&logoColor=white"/>, <img alt="cplusplus" src ="https://img.shields.io/badge/cplusplus-00599C.svg?&style=flat-square&logo=cplusplus&logoColor=white"/>  
> **환경** : <img alt="linux" src ="https://img.shields.io/badge/linux-FCC624.svg?&style=flat-square&logo=linux&logoColor=white"/>,<img alt="ros" src ="https://img.shields.io/badge/ros-22314E.svg?&style=flat-square&logo=ros&logoColor=white"/>, <img alt="raspberrypi" src ="https://img.shields.io/badge/raspberrypi-A22846.svg?&style=flat-square&logo=raspberrypi&logoColor=white"/>, <img alt="arduino" src ="https://img.shields.io/badge/arduino-00979D.svg?&style=flat-square&logo=arduino&logoColor=white"/>  
> **라이브러리** : <img alt="qt" src ="https://img.shields.io/badge/qt-41CD52.svg?&style=flat-square&logo=qt&logoColor=white"/>, <img alt="tensorflow" src ="https://img.shields.io/badge/tensorflow-FF6F00.svg?&style=flat-square&logo=tensorflow&logoColor=white"/>, <img alt="OpenCV" src ="https://img.shields.io/badge/OpenCV-5C3EE8.svg?&style=flat-square&logo=opencv&logoColor=white"/>   
> **도구** : <img alt="github" src ="https://img.shields.io/badge/github-181717.svg?&style=flat-square&logo=github&logoColor=white"/>   


## **✨ 기능 구현**
### **GUI**
<img width="100%" alt="GUI 화면" src="https://github.com/RedCloud79/SSAB/blob/main/GUI/Screenshot%20from%202023-07-20%2014-49-16.png" />

* 물품 선택 및 수량을 입력    
* 입력받은 값을 Vending machine과 Ros로 socket 통신을 통한 연결
-----------------------------------------------------------------------------------
#### [GUI 코드 및 설명](/GUI/Readme.md)    
-----------------------------------------------------------------------------------

### **Vending_machine**
<img width="100%" alt="Vending_machine Cam 화면" src="https://github.com/RedCloud79/SSAB/blob/main/Vending_machine/2023-07-20-154126_1280x720_scrot_002.png" />

* Mobile의 특정 번호를 Cam을 통하여 인식   
* 고유 번호의 인식에 따라 Arduino로 UART통신으로 전달   
* 받은 전달값에 따른 해당 동작 수행
-----------------------------------------------------------------------------------
#### [Vending_machine 코드 및 설명](/Vending_machine/Readme.md)    
-----------------------------------------------------------------------------------
  
### **ROS**
<img width="100%" alt="Rqt_graph 화면" src="https://github.com/RedCloud79/SSAB/blob/main/ROS/Screenshot%20from%202023-07-20%2017-02-30.png" />

* Cam을 활용한 이동체의 제어   
* Qr의 값을 입력받으면 특정 물품 위치 인식   
-----------------------------------------------------------------------------------
#### [ROS 코드 및 설명](/ROS/Readme.md)  
-----------------------------------------------------------------------------------

## **⏰ 일정**

<table>
  <tr>
    <th>   주차   </th>
    <th colspan = "2">진행 계획</th>
  </tr>
  <tr>
    <td>   1주차   </td>
    <td colspan = "2">프로젝트 방향 설정, 팀원 역할 분배</th>
  </tr>
  <tr>
    <td>   2주차   </td>
    <td colspan = "2">Vending_machine 기본동작 설계 및 구성, Mobile 이동체 환경 구성및 설정</td>
  </tr>
  <tr>
    <td></td>
    <td>Vending_machine</td>
    <td>모터 및 초음파 세서를 활용한 동작 설계</td>
  </tr>
  <tr>
    <td></td>
    <td>Moblie 이동체</td>
    <td>ROS 환경 구성 및 이동체 Topic 제어, Pyzbar를 활용한 특정 Qr값을 전달하는 Topic 구성</td>
  </tr>
  <tr>
    <td>   3주차   </td>
    <td colspan = "2">Mobile 이동체 움직임 개선작업, Vending_machine Cam 연동, GUI 설계</td>
  </tr>
  <tr>
    <td></td>
    <td>Vending_machine</td>
    <td>Cam을 활용한 특정 객체 분류</td>
  </tr>
  <tr>
    <td></td>
    <td>Moblie 이동체</td>
    <td>Cam의 Value값을 활용한 움직임 제어</td>
  </tr>
  <tr>
    <td></td>
    <td>GUI</td>
    <td>Vending_machine과 Mobile의 제어를 위한 화면 설계</td>
  </tr>
  <tr>
    <td>   4주차   </td>
    <td colspan = "2">각 기능별 연결 및 오류 수정</td>
  </tr>
  <tr>
    <td></td>
    <td>Vending_machine</td>
    <td>UART 통신을 통한 Cam과 각 센서의 동작의 연결 및 센서동작 수정</td>
  </tr>
  <tr>
    <td></td>
    <td>Moblie 이동체</td>
    <td>Topic들의 값에 대한 움직이의 수정</td>
  </tr>
  <tr>
    <td></td>
    <td>GUI</td>
    <td>소켓 통신을 통한 이동체와 Vending Machine의 결과 확인</td>
  </tr>
</table>




