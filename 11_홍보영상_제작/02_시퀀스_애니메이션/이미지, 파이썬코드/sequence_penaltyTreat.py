from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_penaltyTreat.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정
        x_admin = -2.5         # Admin
        x_penalty = 0.0        # Penalty (중앙)
        x_student = 2.5        # Student
        
        # Y축 좌표
        start_y = 3.2
        
        # [공통] 패널티 상태 확인
        y_check_req = 2.65      # checkPenaltyStatus
        y_check_res = 1.8      # 내역 반환
        
        # [Alt] 패널티 부과 (Red)
        y_alt_req = 0.9        # assignPenalty
        y_alt_res = 0.4        # 등록 완료
        
        # [Else] 패널티 해제/수정 (Orange)
        y_else_req = -0.75      # updatePenalty
        y_else_res = -1.25      # 수정 완료
        
        # [공통] 최종 알림
        y_notify = -2.6        # notifyReportResult

        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치
        pointer.move_to([x_admin, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- [공통 구간] 패널티 상태 조회 ---
        
        # 1. Admin -> Penalty
        self.play(pointer.animate.move_to([x_admin, y_check_req, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_penalty, y_check_req, 0]), run_time=0.8, rate_func=smooth)

        # 2. Penalty -> Admin
        self.play(pointer.animate.move_to([x_penalty, y_check_res, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_admin, y_check_res, 0]), run_time=0.8, rate_func=smooth)
        
        # --- [분기 구간] Alt(부과) vs Else(수정) 동시 제어 ---
        
        # 점 복제 (Else 경로용: 주황색)
        pointer_else = pointer.copy()
        pointer_else[0].set_color(ORANGE)
        pointer_else[1].set_color(ORANGE)
        self.add(pointer_else)

        # [Step A] 수직 이동 (갈라지기)
        self.play(
            pointer.animate.move_to([x_admin, y_alt_req, 0]),      # Red: 부과
            pointer_else.animate.move_to([x_admin, y_else_req, 0]), # Orange: 수정
            run_time=0.8
        )

        # [Step B] 로직 수행 (동시에 Penalty로 이동)
        self.play(
            pointer.animate.move_to([x_penalty, y_alt_req, 0]),
            pointer_else.animate.move_to([x_penalty, y_else_req, 0]),
            run_time=1.0
        )

        # [Step C] 결과 반환 (동시에 Admin으로 복귀)
        self.play(
            pointer.animate.move_to([x_penalty, y_alt_res, 0]),
            pointer_else.animate.move_to([x_penalty, y_else_res, 0]),
            run_time=0.4
        )
        self.play(
            pointer.animate.move_to([x_admin, y_alt_res, 0]),
            pointer_else.animate.move_to([x_admin, y_else_res, 0]),
            run_time=0.8
        )

        # [Step D] 합류 및 알림 준비
        # 두 점 모두 알림 전송 위치로 이동
        self.play(
            pointer.animate.move_to([x_admin, y_notify, 0]),
            pointer_else.animate.move_to([x_admin, y_notify, 0]),
            run_time=0.8
        )
        
        # 두 케이스 모두 처리 완료됨을 강조 (깜빡임)
        self.play(
            Flash(pointer, color=RED, flash_radius=0.5),
            Flash(pointer_else, color=ORANGE, flash_radius=0.5)
        )

        # [Step E] 알림 전송 (Admin -> Student)
        # 겹쳐진 상태로 이동
        self.play(
            pointer.animate.move_to([x_student, y_notify, 0]),
            pointer_else.animate.move_to([x_student, y_notify, 0]),
            run_time=1.5
        )

        # 마무리
        self.play(FadeOut(pointer), FadeOut(pointer_else))