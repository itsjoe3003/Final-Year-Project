import pyautogui
from Classifier_Model import RandomForestClassifier




class Controller:
    prev_hand = None
    right_clicked = False
    left_clicked = False
    double_clicked = False
    dragging = False
    hand_Landmarks = None
    little_finger_down = None
    little_finger_up = None
    index_finger_down = None
    index_finger_up = None
    middle_finger_down = None
    middle_finger_up = None
    ring_finger_down = None
    ring_finger_up = None
    Thump_finger_down = None 
    Thump_finger_up = None
    all_fingers_down = None
    all_fingers_up = None
    index_finger_within_Thumb_finger = None
    middle_finger_within_Thumb_finger = None
    little_finger_within_Thumb_finger = None
    ring_finger_within_Thumb_finger = None
    screen_width, screen_height = pyautogui.size()


    def update_fingers_status():
        Controller.little_finger_down = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[17].y
        Controller.little_finger_up = Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[17].y
        Controller.index_finger_down = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[5].y
        Controller.index_finger_up = Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[5].y
        Controller.middle_finger_down = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[9].y
        Controller.middle_finger_up = Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[9].y
        Controller.ring_finger_down = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[13].y
        Controller.ring_finger_up = Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_down = Controller.hand_Landmarks.landmark[4].y > Controller.hand_Landmarks.landmark[13].y
        Controller.Thump_finger_up = Controller.hand_Landmarks.landmark[4].y < Controller.hand_Landmarks.landmark[13].y
        Controller.all_fingers_down = Controller.index_finger_down and Controller.middle_finger_down and Controller.ring_finger_down and Controller.little_finger_down
        Controller.all_fingers_up = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_up and Controller.little_finger_up
        Controller.index_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[8].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[8].y < Controller.hand_Landmarks.landmark[2].y
        Controller.middle_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[12].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[12].y < Controller.hand_Landmarks.landmark[2].y
        Controller.little_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[20].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[20].y < Controller.hand_Landmarks.landmark[2].y
        Controller.ring_finger_within_Thumb_finger = Controller.hand_Landmarks.landmark[16].y > Controller.hand_Landmarks.landmark[4].y and Controller.hand_Landmarks.landmark[16].y < Controller.hand_Landmarks.landmark[2].y
    

        
    def cursor_moving(hand_sign):

        if hand_sign == 'Open':
                    # Assuming the index finger landmark is at index 8
            index_finger_x = Controller.hand_Landmarks.landmark[14].x
            index_finger_y = Controller.hand_Landmarks.landmark[14].y

            # Map finger coordinates to screen coordinates
            screen_x = int(index_finger_x * Controller.screen_width)
            screen_y = int(index_finger_y * Controller.screen_height)

            # Move the mouse cursor to the fingertip position
            pyautogui.moveTo(screen_x, screen_y, duration=0)
        
        elif hand_sign == 'Close':
            pass


    
    def detect_scrolling(hand_sign):
        if hand_sign == 'Scroll down':
            pyautogui.scroll(-120)
            print("Scrolling DOWN")
        if hand_sign == 'Scroll up':
            pyautogui.scroll(120)
            print("Scrolling UP")
    
    # def detect_speech(hand_sign):
    #     if hand_sign == 'Double click':
    #         pyautogui.scroll(-120)
    #         print("Scrolling DOWN")
    #     if hand_sign == 'Scroll up':
    #         pyautogui.scroll(120)
    #         print("Scrolling UP")
    

    # def detect_zoomming():
    #     zoomming = Controller.index_finger_up and Controller.middle_finger_up and Controller.ring_finger_down and Controller.little_finger_down
    #     window = .05
    #     index_touches_middle = abs(Controller.hand_Landmarks.landmark[8].x - Controller.hand_Landmarks.landmark[12].x) <= window
    #     zoomming_out = zoomming and index_touches_middle
    #     zoomming_in = zoomming and not index_touches_middle
        
    #     if zoomming_out:
    #         pyautogui.keyDown('ctrl')
    #         pyautogui.scroll(-50)
    #         pyautogui.keyUp('ctrl')
    #         print("Zooming Out")

    #     if zoomming_in:
    #         pyautogui.keyDown('ctrl')
    #         pyautogui.scroll(50)
    #         pyautogui.keyUp('ctrl')
    #         print("Zooming In")

    def detect_clicking(hand_sign):
        if hand_sign == 'Left click':
            pyautogui.click()
            Controller.left_clicked = True
            print("Left Clicking")
        else:
            Controller.left_clicked = False
            # pyautogui.mouseUp(button = "left")


        if hand_sign == 'Right click':
            pyautogui.rightClick()
            Controller.right_clicked = True
            print("Right Clicking")
        else:
            Controller.right_clicked = False

        if hand_sign == 'Double click':
            pyautogui.doubleClick()
            Controller.double_clicked = True
            print("Double Clicking")
        else:
            Controller.double_clicked = False

    
    def detect_dragging(hand_sign):
        # Update the hand gesture state
        Controller.update_fingers_status()

        # Initiate dragging if the little finger is down and dragging has not started yet
        if not Controller.dragging and Controller.little_finger_down:
            pyautogui.mouseDown(button="left")
            Controller.dragging = True
            print("Dragging started")

        # Terminate dragging if the little finger is up and dragging has started
        elif Controller.dragging and not Controller.little_finger_down:
            pyautogui.mouseUp(button="left")
            Controller.dragging = False
            print("Dragging ended")


    
    # def detect_dragging(hand_sign):
    #     if not Controller.dragging and Controller.little_finger_down:
    #     # if hand_sign == 'Close':
    #         pyautogui.mouseDown(button = "left")
    #         Controller.dragging = True
    #         print("Dragging")
    #     # elif not Controller.all_fingers_down:
    #     else:
    #         pyautogui.mouseUp(button = "left")
    #         Controller.dragging = False