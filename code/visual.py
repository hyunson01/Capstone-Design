import cv2
import numpy as np
from config import grid_array, board_height_cm, board_width_cm, grid_width, grid_height, cell_size

def grid_ini(rows=12, cols=12):
    return np.zeros((rows, cols), dtype=int)

def grid_tag_visual(grid_visual, tag_info):
    for tag_id, data in tag_info.items():
        coordinates = data["coordinates"]
        tag_grid_x = int(coordinates[0] * grid_width / board_width_cm)
        tag_grid_y = int(coordinates[1] * grid_height / board_height_cm)

        if 0 <= tag_grid_x < grid_visual.shape[1] and 0 <= tag_grid_y < grid_visual.shape[0]:
            cv2.circle(grid_visual, (tag_grid_x, tag_grid_y), 5, (0, 255, 0), -1)

def info_tag(frame, tag_info):
    y_offset = 30
    for idx, (tag_id, data) in enumerate(sorted(tag_info.items())):
        status = data["status"]
        coordinates = data["coordinates"]
        velocity = data["velocity"]
        
        color = (0, 255, 0) if status == "On" else (0, 0, 255)
        cv2.putText(frame,f"ID {tag_id} {status} ({coordinates[0]:.1f}cm, {coordinates[1]:.1f}cm, {velocity[0]:.1f}cm/s, {velocity[1]:.1f}cm/s)",(10, y_offset + idx * 30),cv2.FONT_HERSHEY_SIMPLEX,0.5,color,1)

def trackbar(val):
    pass

def slider_create():
    cv2.namedWindow("Detected Rectangle")
    cv2.createTrackbar("Brightness Threshold", "Detected Rectangle", 120, 255, trackbar)
    cv2.createTrackbar("Min Aspect Ratio", "Detected Rectangle", 10, 20, trackbar)  # 기본값 1.2
    cv2.createTrackbar("Max Aspect Ratio", "Detected Rectangle", 15, 20, trackbar)  # 기본값 1.5

def slider_value():
    brightness_threshold = cv2.getTrackbarPos("Brightness Threshold", "Detected Rectangle")
    min_aspect_ratio = cv2.getTrackbarPos("Min Aspect Ratio", "Detected Rectangle") / 10.0
    max_aspect_ratio = cv2.getTrackbarPos("Max Aspect Ratio", "Detected Rectangle") / 10.0
    return brightness_threshold, min_aspect_ratio, max_aspect_ratio


def grid_visual():
    global grid_array
    grid_visual = np.ones((grid_height, grid_width, 3), dtype=np.uint8) * 255
    
    for i in range(grid_array.shape[0]):
        for j in range(grid_array.shape[1]):
            cell_x = j * cell_size
            cell_y = i * cell_size
            color = (0, 0, 0) if grid_array[i, j] == 1 else (255, 255, 255)
            cv2.rectangle(grid_visual, (cell_x, cell_y), (cell_x + cell_size, cell_y + cell_size), color, -1)

    # 격자선 그리기
    for i in range(grid_array.shape[0] + 1):
        for i in range(grid_array.shape[0] + 1):
            cv2.line(grid_visual, (0, i * cell_size), (grid_width, i * cell_size), (200, 200, 200), 1)

        for j in range(grid_array.shape[1] + 1):
            cv2.line(grid_visual, (j * cell_size, 0), (j * cell_size, grid_height), (200, 200, 200), 1)

    
    return grid_visual

# 마우스 상태 변수
is_mouse_pressed = False
last_toggled = None


def toggle_cell(row, col):
    global grid_array
    grid_array[row, col] = 1 - grid_array[row, col]  # 값 반전

def mouse_callback(event, x, y, flags, param):
    global is_mouse_pressed, last_toggled

    row, col = y // cell_size, x // cell_size
    if not (0 <= row < grid_array.shape[1] and 0 <= col < grid_array.shape[0]):  # 배열 범위 체크
        return

    if event == cv2.EVENT_LBUTTONDOWN:  # 클릭 시작
        is_mouse_pressed = True
        toggle_cell(row, col)
        last_toggled = (row, col)
        cv2.imshow("Grid", grid_visual())

    elif event == cv2.EVENT_MOUSEMOVE and is_mouse_pressed:  # 드래그 중
        if last_toggled != (row, col):  # 같은 칸이면 무시
            toggle_cell(row, col)
            last_toggled = (row, col)
            cv2.imshow("Grid", grid_visual())

    elif event == cv2.EVENT_LBUTTONUP:  # 클릭 해제
        is_mouse_pressed = False
        last_toggled = None