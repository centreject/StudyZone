from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_announcement.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        x_student = -3.5       # Student
        x_notice = 3.6         # Notice
        
        # Y축 설정 (시간 흐름)
        start_y = 2.25          # 시작점
        
        # 메시지별 Y좌표
        y_req = 0.8            # viewNotice()
        y_res = -0.7           # 목록 표시 및 상세 내용 표시

        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.5).scale(2.0)
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
        
        # 1. viewNotice() : Student -> Notice
        # 요청을 보낼 때 조금 더 빠르게 이동 (가벼운 조회 요청)
        move_trace(pointer, x_notice, y_req)
        
        # Notice 객체에서 데이터 로딩 효과 (회전하며 강조)
        # 점이 제자리에서 한 바퀴 돔
        self.play(Rotate(pointer, angle=2*PI, about_point=pointer.get_center()), run_time=0.5)
        self.play(Flash(pointer, color=RED, flash_radius=0.5))
        self.wait(0.2)

        # 2. 목록 및 상세 내용 반환 : Notice -> Student
        # 데이터를 가지고 돌아오는 느낌으로 천천히 이동
        move_trace(pointer, x_student, y_res)

        # Student에게 데이터 도착 강조
        self.play(Indicate(pointer, color=RED, scale_factor=1.5))
        self.wait(1)

        move_trace(pointer, x_student, y_res-1.55)

        # 마무리
        self.play(FadeOut(pointer))