from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지 불러오기
        diagram_img = ImageMobject("sequence_reservation.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        # External System 좌표 추가 (우측 끝)
        x_student = -3.1
        x_reservation = -1
        x_seat = 1.0
        x_external = 3.1
        
        # Y축 설정
        start_y = 3
        step_y = 0.5

        # 3. 레이저 포인터 생성 (빨간 점)
        laser_dot = Dot(color=RED, radius=0.07)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치 설정
        start_pos = np.array([x_student, start_y, 0])
        pointer.move_to(start_pos)
        self.add(pointer)
        self.wait(0.5)

        # --- 애니메이션 함수 (단일 점 이동용) ---
        def move_trace(target_pointer, to_x, to_y, wait_time=0.2):
            current_x = target_pointer.get_center()[0]
            # 1단계: 수직 이동
            if target_pointer.get_center()[1] != to_y:
                self.play(target_pointer.animate.move_to([current_x, to_y, 0]), run_time=0.7, rate_func=linear)
            # 2단계: 수평 이동
            if current_x != to_x:
                self.play(target_pointer.animate.move_to([to_x, to_y, 0]), run_time=0.85, rate_func=smooth)
            if wait_time > 0:
                self.wait(wait_time)

        # --- 시퀀스 시작 ---

        # 1. 예약 요청 (Student -> Reservation)
        y1 = start_y - 0.5
        move_trace(pointer, x_reservation, y1)

        # 2. 좌석 상태 확인 (Reservation -> Seat)
        y2 = y1 - step_y
        move_trace(pointer, x_seat, y2)

        # 3. 상태 반환 (Seat -> Reservation)
        y3 = y2 - step_y
        move_trace(pointer, x_reservation, y3)

        # ====================================================
        # 4. 분기점 (Splitting): [Alt] vs [Else]
        # ====================================================
        
        # 점 복제 (pointer2 생성)
        pointer2 = pointer.copy()
        self.add(pointer2)
        
        # 목표 Y좌표 설정 (Alt는 조금 아래, Else는 더 아래)
        y_alt = y3 - 0.5   # [Alt] 일반 좌석 처리 구간
        y_else = y3 - 1.65  # [Else] 외부 시스템 좌석 처리 구간 (이미지 하단)

        # [동시 동작 1] 수직 이동 (위/아래로 갈라짐)
        self.play(
            pointer.animate.move_to([x_reservation, y_alt, 0]),  # 점1: Alt로 이동
            pointer2.animate.move_to([x_reservation, y_else, 0]), # 점2: Else로 이동
            run_time=0.8,
            rate_func=linear
        )

        # [동시 동작 2] 수평 이동 (로직 수행)
        # 점1 (Alt): 예약 정보 반환 -> Student 쪽으로
        # 점2 (Else): 외부 시스템 연동 -> External System 쪽으로

        self.play(
            pointer.animate.move_to([x_reservation, y_alt, 0]),
            pointer2.animate.move_to([x_external, y_else, 0]),
            run_time=1.2,
            rate_func=smooth
        )
        
        # pnt1 강조 효과, pnt2 external에서 수직으로 이동1
        self.play(
            Flash(pointer, color=RED, flash_radius=0.5),
            pointer2.animate.move_to([x_external, y_else-0.3, 0]),
        )
        self.wait(0.5)

	# pnt1 수직 이동, pnt2 external -> reservation 이동1
        y4 = y_alt - step_y
        self.play(
            pointer.animate.move_to([x_reservation, y4, 0]),
            pointer2.animate.move_to([x_reservation, y_else-0.3, 0]),
            run_time=1.2,
            rate_func=smooth
        )

	# pnt1 student로 수평 이동, pnt2 student에서 수직으로 이동1
        self.play(
            pointer.animate.move_to([x_student, y4, 0]),
            pointer2.animate.move_to([x_reservation, y_else-0.6, 0]),
            run_time=1.2,
            rate_func=smooth
        )

        self.play(FadeOut(pointer))

        self.play(
            pointer2.animate.move_to([x_external, y_else-0.6, 0]),
            run_time=1,
            rate_func=smooth
        )

        self.play(
            pointer2.animate.move_to([x_external, y_else-1.2, 0]),
            run_time=0.5,
            rate_func=smooth
        )

        self.play(
            pointer2.animate.move_to([x_reservation, y_else-1.2, 0]),
            run_time=1,
            rate_func=smooth
        )

        self.play(
            pointer2.animate.move_to([x_reservation, y_else-1.45, 0]),
            run_time=0.5,
            rate_func=smooth
        )
        self.play(
            Flash(pointer2, color=RED, flash_radius=0.5)
        )

        self.play(
            pointer2.animate.move_to([x_reservation, y_else-2.5, 0]),
            run_time=0.8,
            rate_func=smooth
        )

        self.play(
            pointer2.animate.move_to([x_student, y_else-2.35, 0]),
            run_time=0.8,
            rate_func=smooth
        )

        self.play(
            pointer2.animate.move_to([x_student, y_else-2.8, 0]),
            run_time=0.8,
            rate_func=smooth
        )

        self.play(
            Flash(pointer2, color=RED, flash_radius=0.5)
        )

        # 마무리: 두 점 모두 사라짐
        self.play(FadeOut(pointer2))