from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_seatReport.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정
        x_student = -3.7
        x_report = -1.3
        x_penalty = 1.4
        x_admin = 3.8
        
        # Y축 좌표
        start_y = 3.2
        
        # 공통 구간
        y_submit = 2.8
        y_check = 2.2
        y_res = 1.7
        
        # [Alt] 자동 패널티
        y_alt_go = 0.8         # Report -> Penalty
        y_alt_back = 0.3      # Penalty -> Report
        
        # [Else] 관리자 이관
        y_else_go = -0.8       # Report -> Admin
        y_else_back = -1.2     # Admin -> Report
        y_self_call = -2.4     # updateStatus (Self)
        y_final = -3.1         # 최종 알림

        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치
        pointer.move_to([x_student, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- [공통 구간] 신고 접수 ---
        
        # 1. Student -> Report
        self.play(pointer.animate.move_to([x_student, y_submit, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_report, y_submit, 0]), run_time=0.8, rate_func=smooth)

        # 2. Report -> Penalty
        self.play(pointer.animate.move_to([x_report, y_check, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_penalty, y_check, 0]), run_time=0.8, rate_func=smooth)

        # 3. Penalty -> Report
        self.play(pointer.animate.move_to([x_penalty, y_res, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_report, y_res, 0]), run_time=0.8, rate_func=smooth)
        
        # --- [분기 구간] Alt(자동) vs Else(관리자) 동시 제어 ---
        
        # 점 복제 (Else 경로용: 주황색)
        pointer_else = pointer.copy()
        pointer_else[0].set_color(ORANGE)
        pointer_else[1].set_color(ORANGE)
        self.add(pointer_else)

        # [Step A] 수직 이동 (갈라지기)
        # pointer(Alt)는 위쪽 로직으로, pointer_else(Else)는 아래쪽 로직으로 이동
        self.play(
            pointer.animate.move_to([x_report, y_alt_go, 0]),
            pointer_else.animate.move_to([x_report, y_else_go, 0]),
            run_time=0.8
        )

        # [Step B] 수평 이동 (로직 수행)
        # Alt: Report -> Penalty (짧음)
        # Else: Report -> Admin (김 - 관리자에게 전달)
        self.play(
            pointer.animate.move_to([x_penalty, y_alt_go, 0]),
            pointer_else.animate.move_to([x_admin, y_else_go, 0]),
            run_time=1.2
        )

        # [Step C] 결과 반환
        # Alt: Penalty -> Report (패널티 부여 완료)
        # Else: Admin -> Report (상태 대기 반환)
        self.play(
            pointer.animate.move_to([x_penalty, y_alt_back, 0]),
            pointer_else.animate.move_to([x_admin, y_else_back, 0]),
            run_time=0.4
        )
        self.play(
            pointer.animate.move_to([x_report, y_alt_back, 0]),
            pointer_else.animate.move_to([x_report, y_else_back, 0]),
            run_time=1.0
        )

        # [Step D] Else만의 추가 로직 (Self Call)
        # Alt 점은 먼저 끝나서 y_final 위치로 이동해 대기
        # Else 점은 제자리에서 상태 갱신(Self Call) 수행
        
        # Self Call 좌표 계산 ('ㄷ'자 모션)
        p1 = [x_report, y_else_back - 0.7, 0]
        p1_1 = [x_report + 0.6, y_else_back -0.7, 0]
        p2 = [x_report + 0.6, y_self_call, 0]
        p3 = [x_report, y_self_call, 0]

        self.play(
            pointer.animate.move_to([x_report, y_final, 0]), # Alt: 대기 장소로 이동
            pointer_else.animate.move_to(p1),                # Else: Self Call 시작
            run_time=0.5
        )
        
        # Else Self Call 계속
        self.play(pointer_else.animate.move_to(p1_1), run_time=0.5)
        self.play(pointer_else.animate.move_to(p2), run_time=0.5)
        self.play(pointer_else.animate.move_to(p3), run_time=0.3)
        
        # [Step E] 합류 및 알림 전송
        # Else 점도 최종 위치로 이동
        self.play(pointer_else.animate.move_to([x_report, y_final, 0]), run_time=0.5)
        
        # 두 점이 동시에 깜빡임 (처리 완료)
        self.play(
            Flash(pointer, color=RED, flash_radius=0.5),
            Flash(pointer_else, color=ORANGE, flash_radius=0.5)
        )

        # 학생에게 알림 전송 (Report -> Student)
        self.play(
            pointer.animate.move_to([x_student, y_final, 0]),
            pointer_else.animate.move_to([x_student, y_final, 0]),
            run_time=1.5
        )

        # 마무리
        self.play(FadeOut(pointer), FadeOut(pointer_else))