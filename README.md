# Bot Setup and Installation Guide

This guide provides instructions for setting up and running the bot. Follow the steps below to ensure a smooth installation and execution process. This guide assumes you already have access to the configuration files, icon images, and other resources required for the bot.

## Table of Contents


1. [Install Python](#install-python)
2. [Install Required Python Packages](#install-required-python-packages)
3. [Install ADB (Android Debug Bridge)](#install-adb-android-debug-bridge)
4. [Choose Your Android Environment](#choose-your-android-environment)
   * [Option A: Using a Physical Android Device](#option-a-using-a-physical-android-device)
   * [Option B: Using BlueStacks Emulator](#option-b-using-bluestacks-emulator)
5. [Set Up the Project Structure](#set-up-the-project-structure)
6. [Run the Bot](#run-the-bot)
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

Note: Installing the JDK is not required if you are using a physical Android device or BlueStacks emulator.

### For Windows:

* **Download ADB**: [Android SDK Platform Tools for Windows](https://developer.android.com/studio/releases/platform-tools)
* **Extract the ZIP File** to a directory (e.g., `C:\adb`).
* **Add ADB to System PATH**:

  
  1. Go to Control Panel > System > Advanced system settings.
  2. Click on Environment Variables.
  3. Under System variables, select Path and click Edit.
  4. Click New and add `C:\adb`.
* **Verify Installation**:

  ```bash
  adb version
  ```

### For macOS:

* **Download ADB**: [Android SDK Platform Tools for macOS](https://developer.android.com/studio/releases/platform-tools)
* **Extract the ZIP File**.
* **Move platform-tools** to a desired location (e.g., `~/adb`).
* **Add ADB to PATH**:

  ```bash
  export PATH=$PATH:~/adb/platform-tools
  ```
* **Verify Installation**:

  ```bash
  adb version
  ```

### For Linux:

* **Download ADB**: [Android SDK Platform Tools for Linux](https://developer.android.com/studio/releases/platform-tools)
* **Extract the ZIP File**.
* **Move platform-tools** to a desired location (e.g., `~/adb`).
* **Add ADB to PATH**:

  ```bash
  export PATH=$PATH:~/adb/platform-tools
  ```
* **Alternatively, Install via Package Manager**:

  ```bash
  sudo apt-get install android-tools-adb
  ```
* **Verify Installation**:

  ```bash
  adb version
  ```


---

## 4. Choose Your Android Environment

You can run the bot using either a physical Android device or the BlueStacks emulator.

### Option A: Using a Physical Android Device

* **Enable USB Debugging on Your Android Device**:

  
  1. Go to Settings > About phone.
  2. Tap Build number seven times until developer mode is enabled.
  3. Go back to Settings > System > Developer options.
  4. Enable USB debugging.
* **Connect Your Android Device via USB**:

  
  1. Use a USB cable to connect your device to the computer.
  2. Accept the prompt on your device to authorize USB debugging.
  3. Verify connection by running:

     ```bash
     adb devices
     ```

### Option B: Using BlueStacks Emulator

* **Download and Install BlueStacks**: [BlueStacks Official Website](https://www.bluestacks.com/)
* **Set Up BlueStacks**: Sign in with your Google account if prompted and complete any initial setup.
* **Enable ADB Debugging in BlueStacks Settings**:

  
  1. Click on the gear icon (⚙️) in the toolbar to open Settings.
  2. Navigate to Preferences or Advanced settings.
  3. Enable ADB by toggling the switch.
* **Connect to BlueStacks via ADB**:

  
  1. Open Command Prompt or Terminal.
  2. Connect to BlueStacks with the correct port number:

     ```bash
     adb connect 127.0.0.1:<port_number>
     ```
  3. Replace `<port_number>` with the actual port number you found in BlueStacks settings.
  4. Verify connection:

     ```bash
     adb devices
     ```


---

# 봇 설정 및 설치 가이드

이 가이드는 봇을 설정하고 실행하는 방법을 설명합니다. 아래 단계를 따라 설치와 실행을 원활하게 진행하세요. 이 가이드는 구성 파일, 아이콘 이미지 및 기타 필요한 리소스에 이미 액세스할 수 있다고 가정합니다.

## 목차


1. [Python 설치](#python-%EC%84%A4%EC%B9%98)
2. [필요한 Python 패키지 설치](#%ED%95%84%EC%9A%94%ED%95%9C-python-%ED%8C%A8%ED%82%A4%EC%A7%80-%EC%84%A4%EC%B9%98)
3. [ADB (Android Debug Bridge) 설치](#adb-android-debug-bridge-%EC%84%A4%EC%B9%98)
4. [Android 환경 선택](#android-%ED%99%98%EA%B2%BD-%EC%84%A0%ED%83%9D)
   * [옵션 A: 실제 Android 기기 사용](#%EC%98%B5%EC%85%98-a-%EC%8B%A4%EC%A0%9C-android-%EA%B8%B0%EA%B8%B0-%EC%82%AC%EC%9A%A9)
   * [옵션 B: BlueStacks 에뮬레이터 사용](#%EC%98%B5%EC%85%98-b-bluestacks-%EC%97%90%EB%AE%AC%EB%A0%88%EC%9D%B4%ED%84%B0-%EC%82%AC%EC%9A%A9)
5. [프로젝트 구조 설정](#%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B5%AC%EC%A1%B0-%EC%84%A4%EC%A0%95)
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

참고: 실제 Android 기기 또는 BlueStacks 에뮬레이터를 사용하는 경우 JDK를 설치할 필요는 없습니다.

### Windows:

* **ADB 다운로드**: [Android SDK Platform Tools for Windows](https://developer.android.com/studio/releases/platform-tools)
* **ZIP 파일을 디렉토리에 압축 해제** (예: `C:\adb`).
* **ADB를 시스템 PATH에 추가**:

  
  1. 제어판 > 시스템 > 고급 시스템 설정으로 이동합니다.
  2. 환경 변수 클릭.
  3. 시스템 변수에서 Path 선택 후 편집 클릭.
  4. 새로 만들기 클릭 후 `C:\adb` 추가.
* **설치 확인**:

  ```bash
  adb version
  ```

### macOS:

* **ADB 다운로드**: [Android SDK Platform Tools for macOS](https://developer.android.com/studio/releases/platform-tools)
* **ZIP 파일을 압축 해제**.
* **platform-tools를 원하는 위치로 이동** (예: `~/adb`).
* **ADB를 PATH에 추가**:

  ```bash
  export PATH=$PATH:~/adb/platform-tools
  ```
* **설치 확인**:

  ```bash
  adb version
  ```

### Linux:

* **ADB 다운로드**: [Android SDK Platform Tools for Linux](https://developer.android.com/studio/releases/platform-tools)
* **ZIP 파일을 압축 해제**.
* **platform-tools를 원하는 위치로 이동** (예: `~/adb`).
* **ADB를 PATH에 추가**:

  ```bash
  export PATH=$PATH:~/adb/platform-tools
  ```
* **패키지 매니저를 사용한 설치**:

  ```bash
  sudo apt-get install android-tools-adb
  ```
* **설치 확인**:

  ```bash
  adb version
  ```


---

## 4. Android 환경 선택

봇은 실제 Android 기기 또는 BlueStacks 에뮬레이터를 사용하여 실행할 수 있습니다.

### 옵션 A: 실제 Android 기기 사용

* **Android 기기에서 USB 디버깅 활성화**:

  
  1. 설정 > 휴대전화 정보로 이동.
  2. 빌드 번호를 7번 클릭하여 개발자 모드를 활성화.
  3. 설정 > 시스템 > 개발자 옵션으로 돌아가 USB 디버깅을 활성화.
* **USB를 통해 Android 기기 연결**:

  
  1. USB 케이블을 사용하여 기기를 컴퓨터에 연결.
  2. 기기에서 USB 디버깅 허용 요청을 승인.
  3. 연결 확인:

     ```bash
     adb devices
     ```

### 옵션 B: BlueStacks 에뮬레이터 사용

* **BlueStacks 다운로드 및 설치**: [BlueStacks 공식 웹사이트](https://www.bluestacks.com/)
* **BlueStacks 설정**: Google 계정으로 로그인하고 초기 설정을 완료하세요.
* **BlueStacks 설정에서 ADB 디버깅 활성화**:

  
  1. 도구 모음에서 톱니바퀴 아이콘(⚙️) 클릭하여 설정 열기.
  2. 환경 설정 또는 고급 설정으로 이동.
  3. ADB 디버깅을 활성화.
* **ADB를 통해 BlueStacks에 연결**:

  
  1. 명령 프롬프트 또는 터미널을 엽니다.
  2. 올바른 포트 번호를 사용하여 BlueStacks에 연결:

     ```bash
     adb connect 127.0.0.1:<port_number>
     ```
  3. `<port_number>`를 BlueStacks 설정에서 찾은 실제 포트 번호로 대체.
  4. 연결 확인:

     ```bash
     adb devices
     ```


