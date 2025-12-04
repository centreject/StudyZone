from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_useReport.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        x_student = -5.4       # Student
        x_reservation = 1.8    # Reservation
        
        # Y축 설정 (시간 흐름)
        start_y = 2.2          # 시작점
        
        # 메시지별 Y좌표
        y_req = 1.3            # viewRecord()
        y_search = 0.5         # searchReservationHistory() (Self Call 시작)
        y_search_end = -0.2     # (Self Call 끝)
        y_res = -1.5           # 이용 기록 반환

        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치
        pointer.move_to([x_student, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- 애니메이션 함수 ---
        def move_trace(target, to_x, to_y, wait_time=0.2):
            curr_x = target.get_center()[0]
            # 수직 이동
            if target.get_center()[1] != to_y:
                self.play(target.animate.move_to([curr_x, to_y, 0]), run_time=0.5, rate_func=linear)
            # 수평 이동
            if curr_x != to_x:
                self.play(target.animate.move_to([to_x, to_y, 0]), run_time=0.8, rate_func=smooth)
            if wait_time > 0:
                self.wait(wait_time)

        # --- 시퀀스 시작 ---
        
        # 1. viewRecord() : Student -> Reservation
        move_trace(pointer, x_reservation, y_req)

        move_trace(pointer, x_reservation, y_search)

        # 2. searchReservationHistory() : Reservation -> Reservation (Self Call)
        # 오른쪽으로 나갔다가 돌아오는 'ㄷ'자 모션
        p1 = [x_reservation, y_search, 0]          # 시작점 (현재 위치)
        p2 = [x_reservation + 1.0, y_search - 0.2, 0] # 우측으로 나감
        p3 = [x_reservation + 1.0, y_search_end, 0] # 아래로 내려감
        p4 = [x_reservation, y_search_end, 0]   # 다시 돌아옴

        self.play(pointer.animate.move_to(p2), run_time=0.4, rate_func=smooth)
        self.play(pointer.animate.move_to(p3), run_time=0.6, rate_func=linear)
        self.play(pointer.animate.move_to(p4), run_time=0.4, rate_func=smooth)
        
        # DB 조회 중임을 강조 (반짝임)
        self.play(Flash(pointer, color=RED, flash_radius=0.5))
        self.wait(0.3)

        # 3. 이용 기록 및 상세 정보 표시 : Reservation -> Student
        move_trace(pointer, x_student, y_res)

        # 마무리
        self.play(FadeOut(pointer))