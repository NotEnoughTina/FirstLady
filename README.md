# Last War Bot Setup and Installation Guide

This guide provides instructions for setting up and running the Last War bot. Follow these steps carefully to ensure everything is set up correctly for smooth bot operation.

## Table of Contents


1. [Install Python](#install-python)
2. [Install Required Python Packages](#install-required-python-packages)
3. [Install ADB (Android Debug Bridge)](#install-adb-android-debug-bridge)
4. [Choose Your Android Environment](#choose-your-android-environment)
5. [Set Up Virtual Environment](#set-up-virtual-environment)
6. [Running the Bot](#running-the-bot)
7. [Troubleshooting](#troubleshooting)


---

## 1. Install Python

Ensure you have Python 3.6 or higher installed on your machine.

* **Download Python**: [Python Official Website](https://www.python.org/downloads/)
* **Verify Installation**:

  ```bash
  python --version
  ```


---

## 2. Install Required Python Packages

Install the necessary Python packages using pip.

* **Using requirements.txt**:

  ```bash
  pip install -r requirements.txt
  ```
* **Or Install Individually**:

  ```bash
  pip install opencv-python numpy Pillow
  ```


---

## 3. Install ADB (Android Debug Bridge)

Install ADB for Android debugging and communication with your device or emulator. Follow the instructions for your operating system:

### Windows:

* **Download ADB**: [Android SDK Platform Tools for Windows](https://developer.android.com/studio/releases/platform-tools)
* **Extract the ZIP File** to a directory (e.g., `C:\adb`).
* **Add ADB to System PATH** and verify installation by running:

  ```bash
  adb version
  ```

### macOS/Linux:

* **Download ADB**: [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
* **Extract the ZIP File** and add to your PATH, then verify by running:

  ```bash
  adb version
  ```


---

## 4. Choose Your Android Environment

You can run the bot using either a physical Android device or the BlueStacks emulator.

### Option A: Using a Physical Android Device


1. Enable USB Debugging on your Android device:
   * Go to **Settings > About phone**, tap **Build number** 7 times.
   * Go to **Settings > Developer options** and enable **USB Debugging**.
2. Connect your Android device via USB and authorize debugging.

### Option B: Using BlueStacks Emulator


1. Download and install [BlueStacks](https://www.bluestacks.com/).
2. Enable ADB debugging in BlueStacks by going to settings and toggling **ADB**.
3. Connect to BlueStacks using:

   ```bash
   adb connect 127.0.0.1:<port_number>
   ```


---

## 5. Set Up Virtual Environment

Setting up a virtual environment helps manage dependencies and avoid conflicts.

### Steps to Set Up a Virtual Environment:


1. **Create a Virtual Environment**:

   ```bash
   python -m venv venv
   ```
2. **Activate the Virtual Environment**:
   * **Windows**:

     ```bash
     venv\Scripts\activate
     ```
   * **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```
3. **Install Dependencies**:
   Inside the virtual environment, install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```


---

## 6. Running the Bot

Follow these steps to run the bot correctly:


1. **Start the Virtual Environment**:
   * **Windows**:

     ```bash
     venv\Scripts\activate
     ```
   * **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```
2. **Launch the Last War App**:
   * Open the Last War app on your Android device or BlueStacks emulator.
3. **Navigate to the Capitol Buffs Screen**:
   * Ensure that you are on the **Capitol Buffs screen** of the Last War app.
   * **Scroll to the bottom of the screen** if the Capitol is occupied and there are conqueror positions at the top of the screen. This will ensure that the secretary positions are visible and clickable.
4. **Adjust Line 23 in** `main.py` Based on Your UI:
   * If there are additional conqueror positions at the top of the screen, scroll to the bottom and adjust line 23 in `main.py` as follows:

     ```python
     secretary_positions = load_config_section('SecretaryPositions2')
     ```
   * If there are no conqueror positions at the top, set line 23 in `main.py` to:

     ```python
     secretary_positions = load_config_section('SecretaryPositions1')
     ```
5. **Verify and Adjust** `config.ini` for Secretary Positions:
   * You may need to adjust the positions of the secretaries to match the current UI layout. In the **config.ini** file, ensure that the coordinates of the secretary positions align with their positions on your screen. Modify the `[SecretaryPositions]` section to fit your screen layout.

   Example `config.ini`:

   ```ini
   [SecretaryPositions]
   #FirstLady = 15%, 50%
   Strategy = 45%, 50%
   Security = 75%, 50%
   Development = 15%, 75%
   Science = 45%, 75%
   Interior = 75%, 75%
   ```

   Adjust the percentages if the click positions don’t match the location of the secretaries in the game UI.
6. **Run the Script**:
   Navigate to your project directory and run the script:

   ```bash
   python main.py
   ```


---

## 7. Troubleshooting

### ADB Issues:

* Ensure your device or emulator is connected and recognized by ADB.
* Verify by running:

  ```bash
  adb devices
  ```

### Icon Detection Issues:

* Enable `debug=True` in your function calls to get detailed logs.
* Verify that the icon template images are correct and paths are accurate.

### Dependencies:

* Make sure all required Python packages are installed:

  ```bash
  pip install --upgrade --force-reinstall -r requirements.txt
  ```

### Permission Errors:

* Run the script with appropriate permissions. On Unix systems, you may need to use `sudo` for certain commands.


---

# 라스트 워 봇 설치 및 설정 가이드

이 가이드는 라스트 워 봇을 설정하고 실행하는 방법을 설명합니다. 봇이 원활하게 작동하도록 하기 위해 아래의 단계를 따라 주세요.

## 목차


1. [Python 설치](#python-%EC%84%A4%EC%B9%98)
2. [필요한 Python 패키지 설치](#%ED%95%84%EC%9A%94%ED%95%9C-python-%ED%8C%A8%ED%82%A4%EC%A7%80-%EC%84%A4%EC%B9%98)
3. [ADB (Android Debug Bridge) 설치](#adb-android-debug-bridge-%EC%84%A4%EC%B9%98)
4. [Android 환경 선택](#android-%ED%99%98%EA%B2%BD-%EC%84%A0%ED%83%9D)
5. [가상 환경 설정](#%EA%B0%80%EC%83%81-%ED%99%98%EA%B2%BD-%EC%84%A4%EC%A0%95)
6. [봇 실행](#%EB%B4%87-%EC%8B%A4%ED%96%89)
7. [문제 해결](#%EB%AC%B8%EC%A0%9C-%ED%95%B4%EA%B2%B0)


---

## 1. Python 설치

Python 3.6 이상이 설치되어 있는지 확인하세요.

* **Python 다운로드**: [Python 공식 웹사이트](https://www.python.org/downloads/)
* **설치 확인**:

  ```bash
  python --version
  ```


---

## 2. 필요한 Python 패키지 설치

필요한 Python 패키지를 pip을 사용하여 설치합니다.

* **requirements.txt 사용**:

  ```bash
  pip install -r requirements.txt
  ```
* **개별 설치**:

  ```bash
  pip install opencv-python numpy Pillow
  ```


---

## 3. ADB (Android Debug Bridge) 설치

ADB를 설치하여 Android 기기 또는 에뮬레이터와 디버깅 및 통신을 합니다. 운영 체제에 맞는 방법을 따르세요:

### Windows:

* **ADB 다운로드**: [Android SDK Platform Tools for Windows](https://developer.android.com/studio/releases/platform-tools)
* **ZIP 파일을 디렉토리에 압축 해제** (예: `C:\adb`).
* **ADB를 시스템 PATH에 추가**하고 다음 명령어로 설치를 확인:

  ```bash
  adb version
  ```

### macOS/Linux:

* **ADB 다운로드**: [Android SDK Platform Tools](https://developer.android.com/studio/releases/platform-tools)
* **ZIP 파일을 압축 해제**하고 PATH에 추가한 후 다음 명령어로 확인:

  ```bash
  adb version
  ```


---

## 4. Android 환경 선택

봇은 실제 Android 기기 또는 BlueStacks 에뮬레이터를 사용하여 실행할 수 있습니다.

### 옵션 A: 실제 Android 기기 사용


1. Android 기기에서 USB 디버깅 활성화:
   * **설정 > 휴대전화 정보**로 이동하여 **빌드 번호**를 7번 클릭.
   * **설정 > 개발자 옵션**으로 이동하여 **USB 디버깅**을 활성화.
2. Android 기기를 USB로 연결하고 디버깅을 허용.

### 옵션 B: BlueStacks 에뮬레이터 사용


1. [BlueStacks](https://www.bluestacks.com/)을 다운로드하고 설치.
2. BlueStacks 설정에서 ADB 디버깅을 활성화.
3. 다음 명령어로 BlueStacks에 연결:

   ```bash
   adb connect 127.0.0.1:<port_number>
   ```


---

## 5. 가상 환경 설정

가상 환경을 설정하면 종속성 관리를 쉽게 할 수 있습니다.

### 가상 환경 설정 단계:


1. **가상 환경 생성**:

   ```bash
   python -m venv venv
   ```
2. **가상 환경 활성화**:
   * **Windows**:

     ```bash
     venv\Scripts\activate
     ```
   * **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```
3. **종속성 설치**:
   가상 환경 내에서 필요한 Python 패키지를 설치:

   ```bash
   pip install -r requirements.txt
   ```


---

## 6. 봇 실행

봇을 올바르게 실행하려면 아래 단계를 따르세요:


1. **가상 환경 시작**:
   * **Windows**:

     ```bash
     venv\Scripts\activate
     ```
   * **macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```
2. **라스트 워 앱 실행**:
   * Android 기기 또는 BlueStacks 에뮬레이터에서 라스트 워 앱을 실행하세요.
3. **Capitol Buffs 화면으로 이동**:
   * 라스트 워 앱의 **Capitol Buffs 화면**에 있는지 확인하세요. Capitol이 점령된 경우 화면 상단에 정복자 위치가 있으면, 목록 맨 아래로 스크롤하세요.
4. **UI에 따라** `main.py`의 23번째 줄을 조정:
   * 화면 상단에 정복자 위치가 추가되어 있으면:

     ```python
     secretary_positions = load_config_section('SecretaryPositions2')
     ```
   * 상단에 정복자 위치가 없으면:

     ```python
     secretary_positions = load_config_section('SecretaryPositions1')
     ```
5. **config.ini 파일에서 Secretary Positions 조정**:
   * UI에 맞춰 비서 위치를 조정해야 할 수 있습니다. **config.ini** 파일에서 비서 위치 좌표가 화면 레이아웃과 맞는지 확인하고 조정하세요.

   예시 `config.ini`:

   ```ini
   [SecretaryPositions]
   #FirstLady = 15%, 50%
   Strategy = 45%, 50%
   Security = 75%, 50%
   Development = 15%, 75%
   Science = 45%, 75%
   Interior = 75%, 75%
   ```

   클릭 위치가 게임 UI의 비서 위치와 일치하지 않으면 퍼센트를 조정하세요.
6. **스크립트 실행**:
   프로젝트 디렉토리로 이동한 후 스크립트를 실행:

   ```bash
   python main.py
   ```


---

## 7. 문제 해결

### ADB 문제:

* 기기 또는 에뮬레이터가 ADB에서 인식되고 연결되었는지 확인.
* 다음 명령어로 확인:

  ```bash
  adb devices
  ```

### 아이콘 감지 문제:

* 함수 호출에서 `debug=True`를 활성화하여 자세한 로그를 확인하세요.
* 아이콘 템플릿 이미지가 정확하고 경로가 올바른지 확인하세요.

### 종속성 문제:

* 필요한 모든 Python 패키지가 설치되었는지 확인:

  ```bash
  pip install --upgrade --force-reinstall -r requirements.txt
  ```

### 권한 문제:

* 스크립트를 적절한 권한으로 실행하세요. Unix 시스템에서는 특정 명령어에 대해 `sudo`가 필요할 수 있습니다.


---


