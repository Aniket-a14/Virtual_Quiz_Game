import pygame
import cv2
import csv
import mediapipe as mp
import math
import ctypes
import cvzone
import time

# Initialize Pygame
pygame.init()

# Set up screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Front Page")

# Load background image
background_image = pygame.image.load('background.jpg')  # Replace 'background.jpg' with your image file
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up fonts
title_font = pygame.font.Font(None, 64)
button_font = pygame.font.Font(None, 32)

# Function to display text on screen
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

# Main menu loop
def main_menu():
    while True:
        screen.blit(background_image, (10, 10))

        # Draw title
        #draw_text("Game Title", title_font, BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)

        # Draw buttons
        pygame.draw.rect(screen, GREEN, (250, 300, 300, 50))  # Start Button
        pygame.draw.rect(screen, BLUE, (250, 370, 300, 50))   # Settings Button
        pygame.draw.rect(screen, RED, (250, 440, 300, 50))    # Quit Button

        draw_text("Start Game", button_font, BLACK, SCREEN_WIDTH // 2, 325)
        draw_text("Settings", button_font, BLACK, SCREEN_WIDTH // 2, 395)
        draw_text("Quit", button_font, BLACK, SCREEN_WIDTH // 2, 465)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 250 <= mouse_pos[0] <= 550:
                    if 300 <= mouse_pos[1] <= 350:
                        pygame.quit()
                        return "start_game"
                    elif 370 <= mouse_pos[1] <= 420:
                        pygame.quit()
                        return "show_settings"
                    elif 440 <= mouse_pos[1] <= 490:
                        pygame.quit()
                        return "quit"

        pygame.display.flip()

# Function to start the game
def start_game():
    print("Starting game...")  # Placeholder for actual game code

# Function to show settings
def show_settings():
    print("Showing settings...")  # Placeholder for actual settings code

# Initialize video feed and get window resolution
GET_SCREEN_RESOLUTION = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, GET_SCREEN_RESOLUTION[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, GET_SCREEN_RESOLUTION[1])

# Initialize Hand Detection Model
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Simple Distance Calculation hehe
def calculate_distance(p1, p2):
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)

# Function to display "Answer Accepted" on the screen after input is detected
def display_answer_accepted(img):
    img.fill(0) #Create Black Background for Answer Accepted Screen
    text = "Answer Accepted :)"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (img.shape[0] + text_size[1]) // 2
    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
def display_answer_correct(img, correct_choice):
    img.fill(0)  # Create Black Background for Correct Answer Screen
    text = f"Correct Answer: {correct_choice}"
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = (img.shape[1] - text_size[0]) // 2
    text_y = (img.shape[0] + text_size[1]) // 2
    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    


# Create Class for MCQ Data
class MCQ:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = int(data[5])

        self.userAns = None

    # update question frames and create rectangle around
    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.userAns = x + 1
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)


# Import question data
pathCSV = "Mcqs.csv"
with open(pathCSV, newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]
mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))
print("Total MCQ Objects Created:", len(mcqList))
qNo = 0
qTotal = len(dataAll)


# Main loop
while True:
    # Display front page
    action = main_menu()

    # Perform action based on front page selection
    if action == "start_game":
        # Initialize or reset quiz variables
        qNo = 0
        mcqList = []
        for q in dataAll:
            mcqList.append(MCQ(q))
        print("Total MCQ Objects Created:", len(mcqList))

        last_selection_time= 0
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)

            # Detect hands
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)

            # Check if current question is greater than total questions
            if qNo < qTotal:
                mcq = mcqList[qNo]

                # Draw MCQ options
                # Draw MCQ options
                img, bbox1 = cvzone.putTextRect(img, mcq.question, [100, 100], 2, 2,(255,255,255),(0,0,0), offset=30, border=10)
                img, bbox2 = cvzone.putTextRect(img, mcq.choice1, [100, 250], 2, 2,(255,255,255),(0,0,0), offset=20, border=10)
                img, bbox3 = cvzone.putTextRect(img, mcq.choice2, [100, 350], 2, 2,(255,255,255),(0,0,0), offset=20, border=10)
                img, bbox4 = cvzone.putTextRect(img, mcq.choice3, [100, 450], 2, 2,(255,255,255),(0,0,0), offset=20, border=10)
                img, bbox5 = cvzone.putTextRect(img, mcq.choice4, [100, 550], 2, 2,(255,255,255),(0,0,0), offset=20, border=10)


                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0].landmark
                    if len(hand_landmarks) > 13:
                        cursor = (hand_landmarks[8].x * img.shape[1], hand_landmarks[8].y * img.shape[0])
                        distance1 = calculate_distance(hand_landmarks[8], hand_landmarks[12])
                        distance2 = calculate_distance(hand_landmarks[8], hand_landmarks[16])
                        distance3 = calculate_distance(hand_landmarks[8], hand_landmarks[20])
                        if len(hand_landmarks) > 24:
                            distance4 = calculate_distance(hand_landmarks[8], hand_landmarks[24])

                        if distance1 < 35:
                            mcq.update(cursor, [bbox5, bbox2, bbox3, bbox4])
                        elif distance2 < 35:
                            mcq.update(cursor, [bbox2, bbox5, bbox3, bbox4])
                        elif distance3 < 35:
                            mcq.update(cursor, [bbox3, bbox5, bbox2, bbox4])
                        elif distance4 < 35:
                            mcq.update(cursor, [bbox4, bbox5, bbox2, bbox3])

                        if mcq.userAns is not None:
                            current_time = time.time()*1000
                            if current_time-last_selection_time>2000:
                                display_answer_accepted(img)
                                cv2.imshow("Quiz Window", img)
                                cv2.waitKey(2000)
                                correct_choice = mcq.answer
                            
                                display_answer_correct(img, correct_choice)
                                cv2.imshow("Quiz Window", img)
                                cv2.waitKey(2000)
                                
                                last_selection_time=current_time
                                time.sleep(2)
                                qNo += 1
                                continue
                        else:
                            mcq.userAns = None
            
            else:
                score = sum(mcq.answer == mcq.userAns for mcq in mcqList)
                score = round((score / qTotal) * 100, 2)
                img, _ = cvzone.putTextRect(img, "Quiz Completed", [250, 300], 2, 2, offset=50, border=5)
                img, _ = cvzone.putTextRect(img, f'Your Score: {score}%', [700, 300], 2, 2, offset=50, border=5)

            # Draw Progress Bar
            barValue = 150 + (950 // qTotal) * qNo
            cv2.rectangle(img, (150, 600), (barValue, 650), (0, 0, 0), cv2.FILLED)
            cv2.rectangle(img, (150, 600), (1100, 650), (0, 0, 0), 5)
            img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)

            cv2.imshow("Quiz Window", img)
            cv2.setWindowProperty("Quiz Window", cv2.WND_PROP_FULLSCREEN, cv2.WND_PROP_FULLSCREEN)

            # Check for exit key press (ESC)
            key = cv2.waitKey(1)
            if key == 27:
                break

    elif action == "show_settings":
        show_settings()
    elif action == "quit":
        break

# Clean up
cv2.destroyAllWindows()
cap.release()
pygame.quit()
