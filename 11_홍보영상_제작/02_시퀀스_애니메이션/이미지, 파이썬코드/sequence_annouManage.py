from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_annouManage.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정 (이미지상의 Lifeline X좌표)
        x_admin = -1.4         # Admin
        x_notice = 1.4         # Notice
        
        # Y축 설정
        start_y = 3.1          # 시작점
        y_manage = 2.5         # manageNotice (Self Call)
        
        # [Alt] 공지 등록 (Red)
        y_reg_req = 1.5        # createNotice
        y_reg_res = 1.2        # 등록 완료 메시지
        
        # [Else] 공지 수정 (Orange)
        y_mod_req = 0.0        # updateNotice
        y_mod_res = -0.3       # 수정 완료 메시지
        
        # [Else] 공지 삭제 (Yellow)
        y_del_req = -1.5       # deleteNotice
        y_del_res = -1.8       # 삭제 완료 메시지
        
        # 최종 (Self Call)
        y_final = -2.4         # 변경 사항 저장 완료 확인

        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치
        pointer.move_to([x_admin, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- [공통 구간] 공지사항 관리 접근 ---
        # Admin Self Call ('ㄷ'자)
        p1 = [x_admin + 0.6, start_y - 0.2, 0]
        p2 = [x_admin + 0.6, y_manage, 0]
        p3 = [x_admin, y_manage, 0]
        
        self.play(pointer.animate.move_to(p1), run_time=0.3)
        self.play(pointer.animate.move_to(p2), run_time=0.5)
        self.play(pointer.animate.move_to(p3), run_time=0.3)
        self.wait(0.2)
        
        # --- [분기 구간] 3개 트랙 동시 실행 ---
        
        # 점 복제
        pointer_mod = pointer.copy()
        pointer_mod[0].set_color(ORANGE)
        pointer_mod[1].set_color(ORANGE)
        
        pointer_del = pointer.copy()
        pointer_del[0].set_color(YELLOW)
        pointer_del[1].set_color(YELLOW)
        
        self.add(pointer_mod, pointer_del)

        # [Step A] 수직 이동 (3개로 갈라짐)
        self.play(
            pointer.animate.move_to([x_admin, y_reg_req, 0]),     # Red: 등록
            pointer_mod.animate.move_to([x_admin, y_mod_req, 0]), # Orange: 수정
            pointer_del.animate.move_to([x_admin, y_del_req, 0]), # Yellow: 삭제
            run_time=1.2
        )

        # [Step B] Admin -> Notice (요청 전송)
        self.play(
            pointer.animate.move_to([x_notice, y_reg_req, 0]),
            pointer_mod.animate.move_to([x_notice, y_mod_req, 0]),
            pointer_del.animate.move_to([x_notice, y_del_req, 0]),
            run_time=1.0
        )

        # [Step C] Notice -> Admin (결과 반환)
        self.play(
            pointer.animate.move_to([x_admin, y_reg_res, 0]),
            pointer_mod.animate.move_to([x_admin, y_mod_res, 0]),
            pointer_del.animate.move_to([x_admin, y_del_res, 0]),
            run_time=1.0
        )

        # [Step D] 대기 장소로 이동 (순차적 도착 느낌)
        # Red(등록)가 제일 먼저 도착해서 기다림
        self.play(pointer.animate.move_to([x_admin, y_final, 0]), run_time=1.5)
        
        # Orange(수정) 도착
        self.play(pointer_mod.animate.move_to([x_admin, y_final, 0]), run_time=1.0)
        
        # Yellow(삭제) 도착 (이때 다같이 반짝임)
        self.play(
            pointer_del.animate.move_to([x_admin, y_final, 0]),
            Flash(pointer, color=RED, flash_radius=0.5),
            Flash(pointer_mod, color=ORANGE, flash_radius=0.5),
            Flash(pointer_del, color=YELLOW, flash_radius=0.5),
            run_time=0.8
        )

        # [Step E] 최종 Self Call (저장 완료)
        # 3개의 점이 겹쳐서 같이 움직임
        p_final_1 = [x_admin + 0.6, y_final - 0.2, 0]
        p_final_2 = [x_admin + 0.6, y_final - 0.7, 0]
        p_final_3 = [x_admin, y_final - 0.7, 0]
        p_final_4 = [x_admin, y_final - 1, 0]

        self.play(
            pointer.animate.move_to(p_final_1),
            pointer_mod.animate.move_to(p_final_1),
            pointer_del.animate.move_to(p_final_1),
            run_time=0.3
        )
        self.play(
            pointer.animate.move_to(p_final_2),
            pointer_mod.animate.move_to(p_final_2),
            pointer_del.animate.move_to(p_final_2),
            run_time=0.5
        )
        self.play(
            pointer.animate.move_to(p_final_3),
            pointer_mod.animate.move_to(p_final_3),
            pointer_del.animate.move_to(p_final_3),
            run_time=0.3
        )
        self.play(
            pointer.animate.move_to(p_final_4),
            pointer_mod.animate.move_to(p_final_4),
            pointer_del.animate.move_to(p_final_4),
            run_time=0.3
        )

        # 마무리
        self.play(
            FadeOut(pointer), 
            FadeOut(pointer_mod), 
            FadeOut(pointer_del)
        )