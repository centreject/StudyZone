from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_friendCheck.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        x_student = -2.2       # Student
        x_friend = 2.1         # Friend (Friend System/Server)
        
        # Y축 설정 (시간 흐름)
        start_y = 3          # 시작점
        
        # 메시지별 Y좌표
        y_view = 2.5           # viewFriendStatus (Self Call)
        y_view_end = 2.0
        y_list_req = 1.5       # getFriendList
        y_list_res = 0.5       # List<Student> 반환
        
        # [Loop] 구간 Y좌표
        y_loop_req = -1.1      # getFriendStatus
        y_loop_res = -1.9      # status 반환

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
                self.play(target.animate.move_to([curr_x, to_y, 0]), run_time=0.4, rate_func=linear)
            # 수평 이동
            if curr_x != to_x:
                self.play(target.animate.move_to([to_x, to_y, 0]), run_time=0.6, rate_func=smooth)
            if wait_time > 0:
                self.wait(wait_time)

        # --- 시퀀스 시작 ---
        
        # 1. viewFriendStatus() : Self Call
        # 'ㄷ'자 모션
        p1 = [x_student + 0.7, start_y - 0.5, 0]
        p2 = [x_student + 0.7, y_view_end, 0]
        p3 = [x_student, y_view_end, 0]
        
        self.play(pointer.animate.move_to([x_student, start_y - 0.5, 0]), run_time=0.3) # 하강
        self.play(pointer.animate.move_to(p1), run_time=0.3)
        self.play(pointer.animate.move_to(p2), run_time=0.5)
        self.play(pointer.animate.move_to(p3), run_time=0.3)
        
        # 2. getFriendList() : Student -> Friend
        move_trace(pointer, x_friend, y_list_req)

        # 3. List<Student> 반환 : Friend -> Student
        move_trace(pointer, x_student, y_list_res)

        # --- [Loop] 친구 상태 확인 반복 (3회) ---
        
        for i in range(3):
            # 루프 진입 강조 (첫 번째만)
            if i == 0:
                self.play(Flash(pointer, color=RED, flash_radius=0.5))
            
            # 4. getFriendStatus(friend) : Student -> Friend
            # 루프 안에서 조금씩 내려가며 반복하는 느낌을 줄 수도 있지만,
            # 다이어그램 상 위치는 고정되어 있으므로 같은 위치를 왕복합니다.
            move_trace(pointer, x_friend, y_loop_req, wait_time=0.1)
            
            # Friend 쪽에서 처리 중 (잠깐 멈춤)
            self.wait(0.1)

            # 5. status 반환 : Friend -> Student
            move_trace(pointer, x_student, y_loop_res, wait_time=0.1)
            
            # 다음 반복을 위해 위로 살짝 복귀 (Loop 느낌 연출)
            if i < 2:
                self.play(pointer.animate.move_to([x_student, y_loop_req + 0.2, 0]), run_time=0.3, rate_func=linear)

        # 마무리
        self.play(FadeOut(pointer))