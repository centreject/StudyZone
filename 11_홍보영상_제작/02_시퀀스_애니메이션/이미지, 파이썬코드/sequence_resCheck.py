from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_resCheck.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        x_student = -3.1       # Student
        x_reservation = 0.0    # Reservation (가운데)
        x_seat = 3.1           # Seat
        
        # Y축 설정
        start_y = 3.1          # 시작점
        
        # 공통 구간 Y좌표
        y_req = 2.5            
        y_res = 1.8            
        
        # [Alt] 상세 확인 구간 Y좌표
        y_alt_go = 1.1         # Student -> Res
        y_alt_back = 0.8       # Res -> Student
        
        # [Else] 예약 취소 구간 Y좌표
        y_else_go = -0.35       # Student -> Res
        y_else_seat = -0.75     # Res -> Seat (status change)
        y_else_res = -1.5      # Seat -> Res (return)
        y_else_back = -2.0     # Res -> Student
        
        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치
        pointer.move_to([x_student, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- [공통 구간] 예약 목록 조회 (하나의 점) ---
        
        # 1. Student -> Reservation (하강 후 이동)
        self.play(pointer.animate.move_to([x_student, y_req, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_reservation, y_req, 0]), run_time=0.8, rate_func=smooth)

        # 2. Reservation -> Student
        self.play(pointer.animate.move_to([x_reservation, y_res, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_student, y_res, 0]), run_time=0.8, rate_func=smooth)
        
        # --- [분기 구간] Alt(상세) vs Else(취소) 동시 제어 ---
        
        # 3. 분기 시작: 점 복제 (Else 경로용: 주황색)
        pointer_else = pointer.copy()
        pointer_else[0].set_color(ORANGE) 
        pointer_else[1].set_color(ORANGE)
        self.add(pointer_else)

        # [Step A] 수직 이동 (각자의 블록 높이로 이동)
        self.play(
            pointer.animate.move_to([x_student, y_alt_go, 0]),        # 점1: Alt 높이로
            pointer_else.animate.move_to([x_student, y_else_go, 0]),  # 점2: Else 높이로
            run_time=0.8
        )

        # [Step B] 수평 이동 (동시에 Request 전송: Student -> Reservation)
        self.play(
            pointer.animate.move_to([x_reservation, y_alt_go, 0]),
            pointer_else.animate.move_to([x_reservation, y_else_go, 0]),
            run_time=1.0
        )

        # [Step C] 갈라지는 로직
        # Alt(점1): 바로 Student로 반환 (빠름)
        # Else(점2): Seat으로 이동 (더 깊은 로직)
        self.play(
            pointer.animate.move_to([x_reservation, y_alt_back, 0]), # Alt: 하강 준비
            pointer_else.animate.move_to([x_reservation, y_else_seat, 0]), # Else: 하강 준비
            run_time=0.5
        )
        
        self.play(
            pointer.animate.move_to([x_student, y_alt_back, 0]),     # Alt: Student로 반환 (끝)
            pointer_else.animate.move_to([x_seat, y_else_seat, 0]),  # Else: Seat으로 이동
            run_time=1.0
        )

        # [Step D] Else 나머지 로직 수행 (Alt 점은 대기)
        # Else: Seat -> Reservation
        self.play(
            Flash(pointer, color=RED, flash_radius=0.5, run_time=0.5), # Alt 완료 깜빡임
            pointer_else.animate.move_to([x_seat, y_else_res, 0]),
            run_time=0.5
        )
        self.play(
            pointer_else.animate.move_to([x_reservation, y_else_res, 0]),
            run_time=0.8
        )

        # [Step E] Else 최종 반환
        # Else: Reservation -> Student
        self.play(
            pointer_else.animate.move_to([x_reservation, y_else_back, 0]),
            run_time=0.4
        )
        self.play(
            pointer_else.animate.move_to([x_student, y_else_back, 0]),
            run_time=0.8
        )
        self.play(
            pointer_else.animate.move_to([x_student, y_else_back-0.45, 0]),
            run_time=0.3
        )        
        self.play(
            pointer_else.animate.move_to([x_student+0.4, y_else_back-0.45, 0]),
            run_time=0.3
        )
        self.play(
            pointer_else.animate.move_to([x_student+0.4, y_else_back-0.8, 0]),
            run_time=0.3
        )
        self.play(
            pointer_else.animate.move_to([x_student, y_else_back-0.8, 0]),
            run_time=0.3
        )
        # 마지막 강조
        self.play(Flash(pointer_else, color=ORANGE, flash_radius=0.5))
        self.wait(0.5)

        # 마무리
        self.play(FadeOut(pointer), FadeOut(pointer_else))