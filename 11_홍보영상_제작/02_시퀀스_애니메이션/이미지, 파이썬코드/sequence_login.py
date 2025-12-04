from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지 불러오기
        # 업로드하신 파일명과 동일해야 합니다.
        diagram_img = ImageMobject("sequence_login.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        # 이미지를 보고 대략적인 위치를 잡았습니다. 실행 후 미세 조정하세요.
        x_student = -2.4  # Student (왼쪽)
        x_user = 0.35      # User (오른쪽)
        
        # Y축 설정 (위에서부터 아래로 내려갈 높이들)
        start_y = 3     # 시작점 (맨 위)
        y_req = 2.5       # login 요청
        y_verify = 1.8    # verifyCredentials (Self Call)
        
        # [Alt] 성공 블록 좌표
        y_alt_start = 1
        y_alt_token = -0.5
        y_alt_end = 0

        # [Else] 실패 블록 좌표
        y_else_start = -0.5
        y_else_end = -2

        # 3. 레이저 포인터 생성 (빨간 점)
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치 (Student 라인 시작점)
        pointer.move_to([x_student, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- [공통 구간] 로그인 요청 및 검증 ---
        
        # 1. login(id, password) : Student -> User
        self.play(pointer.animate.move_to([x_student, y_req, 0]), run_time=0.5, rate_func=linear) # 하강
        self.play(pointer.animate.move_to([x_user, y_req, 0]), run_time=1.0, rate_func=smooth)    # 이동

        # 2. verifyCredentials() : User -> User (Self Call)
        # 오른쪽으로 살짝 나갔다가 돌아오는 'ㄷ'자 모양 연출
        p1 = [x_user, y_req - 0.5, 0]
        p1_1 = [x_user + 0.5, y_req - 0.5, 0]
        p2 = [x_user + 0.5, y_verify, 0]
        p3 = [x_user, y_verify, 0]
        p3_1 = [x_user, y_verify - 0.6, 0]
        
        self.play(pointer.animate.move_to(p1), run_time=0.3)
        self.play(pointer.animate.move_to(p1_1), run_time=0.3)
        self.play(pointer.animate.move_to(p2), run_time=0.5)
        self.play(pointer.animate.move_to(p3), run_time=0.3)
        
        # 처리 중 반짝임 효과
        self.play(Flash(pointer, color=RED, flash_radius=0.5))
        self.wait(0.3)

        self.play(pointer.animate.move_to(p3_1), run_time=0.3)

        # --- [분기 구간] Alt(성공) vs Else(실패) 동시 실행 ---
        
        # 점 복제 (실패 경로용)
        pointer_fail = pointer.copy()
        pointer_fail.set_color(ORANGE) # 구분을 위해 색상 변경 (선택사항)
        self.add(pointer_fail)

        # [Track 1] Alt 경로 (인증 성공)
        anim_success = Succession(
            # Alt 블록 진입
            pointer.animate.move_to([x_user, y_alt_start, 0]).set_run_time(0.5),
            # 인증 성공 응답 (User -> Student)
            pointer.animate.move_to([x_student, y_alt_start, 0]).set_run_time(1.0),
            # 토큰 생성 (다시 User 쪽으로 살짝 이동했다가 돌아옴 - 내부 로직 표현)
            pointer.animate.move_to([x_user, y_alt_token, 0]).set_run_time(0.8),
            # 최종 로그인 완료 (User -> Student)
            pointer.animate.move_to([x_student, y_alt_end, 0]).set_run_time(1.0)
        )

        # [Track 2] Else 경로 (인증 실패)
        anim_fail = Succession(
            # Else 블록까지 쭉 내려감 (시간차)
            pointer_fail.animate.move_to([x_user, y_else_start, 0]).set_run_time(2.0),
            # 에러 메시지 반환 (User -> Student)
            pointer_fail.animate.move_to([x_student, y_else_start, 0]).set_run_time(1.0),
            # 로그인 화면 복귀 (Self Call)
            pointer_fail.animate.move_to([x_student + 0.5, y_else_start - 0.2, 0]).set_run_time(0.3),
            pointer_fail.animate.move_to([x_student + 0.5, y_else_end, 0]).set_run_time(0.5),
            pointer_fail.animate.move_to([x_student, y_else_end, 0]).set_run_time(0.3)
        )

        # 두 트랙 동시 실행
        self.play(AnimationGroup(anim_success, anim_fail), run_time=5.5)
        
        # 마무리
        self.play(FadeOut(pointer), FadeOut(pointer_fail))