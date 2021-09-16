1. makeStream.py
  1) 프로그램 기능
      - 같은 폴더에 있는 'test.yml'파일을 읽고 비트스트림을 만들어 시리얼 통신을 통해 아두이노로 보낸다.
      - 비트스트림은 MSB first 기준으로 만든다.
  2) 실행환경
       - 윈도우, python3, PyYAML모듈, PySerial모듈이 필요하다.
       - idle: 기본 python idle가능, vscode는 Python, Python for VSCode extension이 설치되어 있는 상황에서 실행함.
  3) 프로그램 실행 단계
     step1: test.yml 파일 읽어오기
     step2: 시리얼 통신 연결 및 초기화
     step3: test.yml 에서 읽어온 데이터로 비트스트림 생성 및 아두이노로 송신
     step4: 올바른 데이터를 보냈는지 체크
     step5: 아두이노에서 칩으로 데이터를 보냈는지 체크
     step6: 모두 정상이면 step3으로 돌아가 반복

2. 파이썬 모듈 설치 방법 (윈도우 기준)
    step1: cmd를 관리자 권한으로 실행
    step2: pip install PyYAML 입력
    step3: pip install PySerial 입력
    
   #설치가 안될 시
      1) pip PATH가 설정돼있는지 확인
         -> 저의 경우 C:\Users\UserName\AppData\Local\Programs\Python\Python38\Scripts
         보통 Python\Python38\Script 에 저장되어 있음
         $아나콘다의 경우 c:\ProgramData\Anaconda3\Scripts 단 아나콘다로 실행해본 적은 없음
      2) pip가 설치돼있는지 확인
          주의사항: 'venv\Lib' 이런 경로에 있는 파일이 아니라 위 경로와 비슷한 경로에 설치돼있어야 함
                        만약 안돼있다면 아래 링크 참조
                        https://dora-guide.com/pip-install/
       3)설치 후, 1) pip PATH 다시 시도

3. 시리얼 포트 설정
    step1: 아두이노와 컴퓨터 usb연결
    step2: 장치 관리자 -> 포트 -> Arduino Uno(COMx) -> 포트 설정
    step3: 설정 내용 -> 비트/초: 115200, 데이터 비트: 8, 패리티: 없음, 정지 비트: 1, 흐름 제어: 없음

4. dataTransfer.ino
    1) 시리얼 통신을 통해 비트스트림을 컴퓨터로부터 받아오고 그 스트림을 칩에 보낸다.
    2) 실행 환경: 아두이노 우노, SPI.h 모듈 필요(웬만해선 아두이노 ide 설치할 때 기본으로 깔려있음)
    3) 프로그램 실행순서
       step1: 변수, 핀, 통신 초기화
       step2: 컴퓨터에서 시리얼 통신으로 데이터가 올 때 까지 대기
       step3: 받은 값 컴퓨터에 재전송(재대로 받았는 지 확인하기 위해서)
       step4: 받아온 비트스트림을 SPI통신을 통해 칩으로 전송
       step5: 컴퓨터에 SPI통신이 끝났음을 알림
       step6: step2로 돌아감
   
    4) CLK, DATA, EN, RST핀:
        - CLK: 13번핀, DATA: 11번핀, EN: 10번핀, RST: 9번핀
        - 초기 상태  -> CLK : IDLE,  DATA: X,  EN: LOW,  RST: LOW
        - SPI 통신단계
           step1: 통신시작 전 RST핀에서 펄스 출력
           step2: EN핀을 HIGH로 올리고 데이터 전송 시작
           step3: 데이터 전송 후 EN핀을 LOW로 내리고 통신 끝
  
  5) 수정해줘야 하는 변수: 
       1.  _MAXBYTES: 한번에 보내고 싶은 최대 바이트 수 -> 최대 255까지 가능( 더 늘리고 싶다면 코드를 수정해야 함)
       2.  SPI_MODE: clk의 idle 값, falling/rising edge transfer 를 정할 수 있다. 
          - SPI_MODE0: CLK idle = low, bit transfer = rising edge
          - SPI_MODE1: CLK idle = low, bit transfer = falling edge
          - SPI_MODE2: CLK idle = HIGH, bit transfer = falling edge
          - SPI_MODE3: CLK idle = HIGH, bit transfer = rising edge
       3. MSBFIRST/LSBFIRST -> most/least significant bit first

5. test.yml:
   1) 기능: 비트를 입력하는 입력파일 
   2) YAML형식의 마크다운 언어로 작성됨.
   3) 작성형식

Stream1:
  1: [ 0, 0, 0, 0, 0, 0, 0, 1 ]
  2: [ 0, 0, 0, 0, 0, 0, 1, 0 ]
  3: [ 0, 0, 0, 0, 0, 0, 1, 1 ]
   ....
  n1: [ 0, 1, 0, 0, 0, 0, 0, 0 ]
Stream2:
  1: [ 0, 0, 0, 0, 0, 0, 0, 1 ]
  2: [ 0, 0, 0, 0, 0, 0, 1, 0 ]
  3: [ 0, 0, 0, 0, 0, 0, 1, 1 ]
   ....
   n2: [ 0, 1, 0, 0, 0, 0, 0, 0 ]
 .......
StreamN:
   1: [ 0, 0, 1, 0, 0, 1, 0, 0 ]
   2: [ 0, 0, 1, 0, 0, 1, 0, 1 ]
   3: [ 0, 0, 1, 0, 0, 1, 1, 0 ]
   ....
   nN: [ 0, 0, 1, 1, 0, 0, 1, 0 ]

   4) 작성 시 주의 사항
       - n의 최대 값: 255, N은 최대 값이 없음 (int 범위)
       - 상위 라벨 StreamX들은 이름을 바꿔도 상관 없다. 다만 indent(들여쓰기)는 같아야 하고 단순 숫자( ex: '1' ) 는 따옴표료 묶어야 함
          ex)
'1':
  1: [ 0, 0, 0, 0, 0, 0, 0, 1 ]
  2: [ 0, 0, 0, 0, 0, 0, 1, 0 ]
  3: [ 0, 0, 0, 0, 0, 0, 1, 1 ]
   ....
  n1: [ 0, 1, 0, 0, 0, 0, 0, 0 ]

   5) 비트스트림 순서: 
       - 왼쪽 비트 부터 전송됨( MSBFIRST ) 
       - nX: [ 0, 1 ... , 0 ] <- 여기가 마지막으로 전송됨

6. 기타 주의사항:
      저는 아두이노를 연결한 상태에서 파이썬 프로그램만 실행해도 아두이노가 알아서 처음부터 동작했지만혹시 에러가 생길 경우 
      아두이노를 먼저 리셋해주고(빨간 버튼) 파이썬 프로그램을 실행해주시면 됩니다.
    
        
