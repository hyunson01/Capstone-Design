import cv2
import numpy as np
import os
import json



# 설정
GRID_SIZE = 10
CELL_SIZE = 50  # 한 칸 크기 (픽셀)
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
FILENAME = r"D:\git\Capstone-Design"  # JSON 파일 경로 (역슬래시 오류 방지: r"" 사용)

# JSON에서 배열 불러오기
def load_grid(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            return np.array(data["grid"], dtype=int)  # JSON의 grid 부분을 로드
    else:
        return np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)  # 파일 없으면 0으로 초기화

# JSON으로 배열 저장
def save_grid(grid):
    filename=FILENAME
    data = {
        "grid": grid.tolist()  # numpy 배열을 리스트로 변환하여 저장
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)  # 보기 좋게 저장
    print(f"저장 완료: {filename}")

# 현재 상태 저장할 배열 불러오기
grid = load_grid(FILENAME)

# 색상 설정
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GRID = (200, 200, 200)



# 창 생성 및 초기 화면 표시
cv2.namedWindow("Grid")
cv2.setMouseCallback("Grid", mouse_callback)
cv2.imshow("Grid", draw_grid())

# 키 입력 대기
while True:
    key = cv2.waitKey(1)

    if key == ord('s'):  # 's' 키 -> 배열 저장
        save_grid(FILENAME, grid)

    elif key == ord('q'):  # 'q' 키 -> 종료 (저장 없이)
        break

cv2.destroyAllWindows()
