from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_reportTreat.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정
        x_admin = -4.85         # Admin
        x_report = -1.6        # Report
        x_penalty = 1.65        # Penalty
        x_student = 4.35        # Student
        
        # Y축 좌표
        start_y = 3.2
        
        # [Opt] 대기 상태 확인
        y_opt_req = 2.35        # viewReportDetail
        
        # [Alt] 유효한 신고 (Red)
        y_alt_req = 1.4        # assignPenalty
        y_alt_res = 1        # 패널티 부여 완료
        y_alt_update = 0.7    # updateStatus
        y_alt_fin = 0.35       # 상태 갱신 완료
        
        # [Else] 무효한 신고 (Orange)
        y_else_update = -0.9   # updateStatus
        y_else_fin = -1.6      # 상태 갱신 완료
        
        # 최종 알림
        y_notify = 0.15        # notifyReportResult (화살표가 Alt 블록 안에서 시작됨)
        y_end = -4.0

        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치
        pointer.move_to([x_admin, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- [Opt] 관리자 신고 상세 조회 ---
        
        # Admin -> Report
        self.play(pointer.animate.move_to([x_admin, y_opt_req, 0]), run_time=0.4, rate_func=linear)
        self.play(pointer.animate.move_to([x_report, y_opt_req, 0]), run_time=0.8, rate_func=smooth)
        
        # Report 조회 중 (반짝임)
        self.play(Flash(pointer, color=RED, flash_radius=0.5))
        self.wait(0.2)
        
        # --- [분기 구간] Alt(유효) vs Else(무효) 동시 제어 ---
        
        # 점 복제 (Else 경로용: 주황색)
        pointer_else = pointer.copy()
        pointer_else[0].set_color(ORANGE)
        pointer_else[1].set_color(ORANGE)
        
        # 시작점 (Admin에서 갈라짐)
        pointer.move_to([x_admin, y_opt_req - 0.5, 0])      # Alt용 점 위치 재조정
        pointer_else.move_to([x_admin, y_opt_req - 0.5, 0]) # Else용 점 위치 재조정
        self.add(pointer, pointer_else)

        # [Step A] 수직 이동 (갈라지기)
        self.play(
            pointer.animate.move_to([x_admin, y_alt_req, 0]),      # Red: Alt 시작점
            pointer_else.animate.move_to([x_admin, y_else_update, 0]), # Orange: Else 시작점
            run_time=1.0
        )

        # [Step B] 로직 수행
        # Alt: Admin -> Penalty (패널티 부여)
        # Else: Admin -> Report (상태 갱신)
        self.play(
            pointer.animate.move_to([x_penalty, y_alt_req, 0]),
            pointer_else.animate.move_to([x_report, y_else_update, 0]),
            run_time=1.0
        )

        # [Step C] 결과 반환 및 후속 처리
        # Alt: Penalty -> Admin (완료) -> Report (상태갱신)
        # Else: Report -> Admin (완료) -> 대기
        self.play(
            pointer.animate.move_to([x_admin, y_alt_res, 0]), # Alt: 반환
            pointer_else.animate.move_to([x_admin, y_else_fin, 0]), # Else: 반환
            run_time=0.6
        )
        
        # Alt 추가 로직: Admin -> Report (상태 갱신)
        self.play(
            pointer.animate.move_to([x_admin, y_alt_update, 0]), # 하강
            run_time=0.3
        )
        self.play(
            pointer.animate.move_to([x_report, y_alt_update, 0]), # 이동
            run_time=0.6
        )
        self.play(
            pointer.animate.move_to([x_admin, y_alt_fin, 0]),     # 반환
            run_time=0.5
        )

        # [Step D] 알림 전송 (유효한 경우만)
        # Alt 점이 notifyReportResult 실행
        self.play(
            pointer.animate.move_to([x_admin, y_notify, 0]), # 하강
            run_time=0.4
        )
        self.play(
            pointer.animate.move_to([x_student, y_notify, 0]), # Student에게 알림
            run_time=1.2
        )
        
        self.play(
            pointer_else.animate.move_to([x_admin, y_else_fin-1, 0]), # Else: 반환
            run_time=0.6
        )

        # Else 점은 사라짐 (무효 처리 끝)
        self.play(FadeOut(pointer_else))
        
        # 마지막 강조
        self.play(Flash(pointer, color=RED, flash_radius=0.5))
        self.wait(0.5)

        # 마무리
        self.play(FadeOut(pointer))