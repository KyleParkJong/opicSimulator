# OPIc Simulator
 오픽 시뮬레이터
 
 ---
 
 * OPIc is an Internet-based (iBT) candidate-friendly foreign language speaking evaluation that makes it as close as possible to OPI, a 1:1 interview evaluation, and is not just a test to measure how much grammar and vocabulary you know, but an objective language evaluation tool to measure how effectively and appropriately you can use language in real life.

 * url : https://m.opic.or.kr/opics/servlet/controller.opic.site.main.MainServlet?p_process=move-init-mobile&p_section=2
 
 ---
 
 ### How to use
 - Start "opic_sim_starter.py"
 - Press start button to start
 - The recording starts as soon as Eva finishes talking, so answer the question right away
 - After talking, your answer will be saved as .wav file and .txt file
 
 ### You can set
 - Number of Questions
 - Answer time per question
 - You can add extra Questions in the list

 ### Used Modules
 - TTS (Text to Speech)
   + import gtts
 - ARS 
   + import SpeechRecognition
 - PyQt5 
   + import pyqt5
