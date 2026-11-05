from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지 불러오기
        # 업로드하신 파일명과 동일해야 합니다.
        diagram_img = ImageMobject("sequence_search.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        # 실행 후 점이 선에서 벗어나면 이 x값들을 조금씩 수정하세요.
        x_student = -5.8       # Student (왼쪽 끝)
        x_reservation = -1.85   # Reservation
        x_sensor = 2.0         # SensorSystem
        x_seat = 5.85           # Seat (오른쪽 끝)
        
        # Y축 설정 (위에서부터 아래로 내려갈 높이들)
        start_y = 3     # 시작점 (맨 위)
        
        # 각 메시지별 Y좌표 (이미지 보며 어림잡음)
        y_req_view = 2.25       # viewReservationInfo
        y_req_sensor = 1.45     # requestSeatStatus
        y_res_sensor = 0.8     # seatStatusData (점선 반환)
        y_update_seat = -0.5   # status 갱신
        y_res_seat = -1.2      # status 반환
        y_res_final = -1.9    # 좌석 현황 데이터 반환
        y_self_call = -3.2     # viewSeatStatus (Self Call)

        # 3. 레이저 포인터 생성 (빨간 점)
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치 (Student 라인 시작점)
        pointer.move_to([x_student, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- 애니메이션 함수 (직각 이동) ---
        def move_trace(to_x, to_y, wait_time=0.2):
            current_x = pointer.get_center()[0]
            # 1단계: 수직 이동
            if pointer.get_center()[1] != to_y:
                self.play(pointer.animate.move_to([current_x, to_y, 0]), run_time=0.5, rate_func=linear)
            # 2단계: 수평 이동
            if current_x != to_x:
                self.play(pointer.animate.move_to([to_x, to_y, 0]), run_time=0.8, rate_func=smooth)
            if wait_time > 0:
                self.wait(wait_time)

        # --- 시퀀스 시작 ---

        # 1. viewReservationInfo() : Student -> Reservation
        move_trace(x_reservation, y_req_view)

        # 2. requestSeatStatus() : Reservation -> SensorSystem
        move_trace(x_sensor, y_req_sensor)

        # 3. seatStatusData : SensorSystem -> Reservation (반환)
        move_trace(x_reservation, y_res_sensor)
        
        # Reservation에서 데이터 처리 중임을 강조 (잠깐 멈춤)
        self.play(Flash(pointer, color=RED, flash_radius=0.5))
        self.wait(0.2)

        # 4. status 갱신 : Reservation -> Seat
        move_trace(x_seat, y_update_seat)

        # 5. status 반환 : Seat -> Reservation
        move_trace(x_reservation, y_res_seat)

        # 6. 좌석 현황 데이터 반환 : Reservation -> Student
        move_trace(x_student, y_res_final)

        # 7. viewSeatStatus() : Student -> Student (Self Call)
        # 'ㄷ'자 모양으로 Self Call 표현
        p1 = [x_student + 0.5, y_res_final - 0.2, 0]
        p2 = [x_student + 0.5, y_self_call, 0]
        p3 = [x_student, y_self_call, 0]
        
        self.play(pointer.animate.move_to(p1), run_time=0.3)
        self.play(pointer.animate.move_to(p2), run_time=0.5)
        self.play(pointer.animate.move_to(p3), run_time=0.3)
        
        # 마지막 강조
        self.play(Flash(pointer, color=RED, flash_radius=0.5))
        self.wait(1)

        # 사라지기
        self.play(FadeOut(pointer))