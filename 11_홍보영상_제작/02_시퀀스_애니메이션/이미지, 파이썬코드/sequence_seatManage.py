from manim import *

class SequenceDiagramAnim(Scene):
    def construct(self):
        # 1. 배경 이미지
        diagram_img = ImageMobject("sequence_seatManage.png")
        diagram_img.height = config.frame_height * 0.95
        self.add(diagram_img)

        # 2. 좌표 설정
        x_admin = -2.7
        x_seat = 0.0
        x_sensor = 2.6
        
        # Y축 좌표
        start_y = 2.9
        y_manage = 2.3         # Self Call
        
        # [Alt] 좌석 추가 (Red)
        y_add_req = 1.5        # Admin -> Seat
        y_add_sensor = 1.2     # Seat -> Sensor
        y_add_res = 0.8        # Sensor -> Seat
        y_add_fin = 0.5        # Seat -> Admin
        
        # [Else] 좌석 삭제 (Orange)
        y_del_req = 0       # Admin -> Seat
        y_del_sensor = -0.3    # Seat -> Sensor
        y_del_res = -0.5       # Sensor -> Seat
        y_del_fin = -0.8       # Seat -> Admin
        
        # [Else] 좌석 수정 (Yellow)
        y_mod_req = -1.4       # Admin -> Seat
        y_mod_fin = -1.8       # Seat -> Admin
        
        # 최종
        y_final = -2.75

        # 3. 레이저 포인터 생성
        laser_dot = Dot(color=RED, radius=0.1)
        laser_glow = laser_dot.copy().set_opacity(0.33).scale(1.8)
        pointer = VGroup(laser_dot, laser_glow)
        
        # 초기 위치
        pointer.move_to([x_admin, start_y, 0])
        self.add(pointer)
        self.wait(0.5)

        # --- [공통 구간] 관리자 기능 접근 ---
        # Admin Self Call
        p1 = [x_admin + 0.6, start_y - 0.2, 0]
        p2 = [x_admin + 0.6, y_manage, 0]
        p3 = [x_admin, y_manage, 0]
        
        self.play(pointer.animate.move_to(p1), run_time=0.3)
        self.play(pointer.animate.move_to(p2), run_time=0.5)
        self.play(pointer.animate.move_to(p3), run_time=0.3)
        
        # --- [분기 구간] 3개 트랙 동시 실행 ---
        
        # 점 복제
        pointer_del = pointer.copy()
        pointer_del[0].set_color(ORANGE)
        pointer_del[1].set_color(ORANGE)
        
        pointer_mod = pointer.copy()
        pointer_mod[0].set_color(YELLOW)
        pointer_mod[1].set_color(YELLOW)
        
        self.add(pointer_del, pointer_mod)

        # [Step A] 수직 이동 (3개로 갈라짐)
        self.play(
            pointer.animate.move_to([x_admin, y_add_req, 0]),     # Red: 추가
            pointer_del.animate.move_to([x_admin, y_del_req, 0]), # Orange: 삭제
            pointer_mod.animate.move_to([x_admin, y_mod_req, 0]), # Yellow: 수정
            run_time=0.8
        )

        # [Step B] Admin -> Seat (동시에 이동)
        self.play(
            pointer.animate.move_to([x_seat, y_add_req, 0]),
            pointer_del.animate.move_to([x_seat, y_del_req, 0]),
            pointer_mod.animate.move_to([x_seat, y_mod_req, 0]),
            run_time=1.0
        )

        # [Step C] 갈라지는 로직
        # Red(추가) & Orange(삭제) : Seat -> Sensor (더 감)
        # Yellow(수정) : Seat -> Admin (바로 복귀)
        self.play(
            pointer.animate.move_to([x_sensor, y_add_sensor, 0]),
            pointer_del.animate.move_to([x_sensor, y_del_sensor, 0]),
            pointer_mod.animate.move_to([x_admin, y_mod_fin, 0]),
            run_time=1.2
        )

        # [Step D] Sensor 반환 로직
        # Red & Orange : Sensor -> Seat -> Admin
        # Yellow : 대기 장소로 이동
        self.play(
            pointer.animate.move_to([x_seat, y_add_res, 0]),
            pointer_del.animate.move_to([x_seat, y_del_res, 0]),
            pointer_mod.animate.move_to([x_admin, y_final, 0]), # Yellow 대기
            run_time=0.8
        )
        
        self.play(
            pointer.animate.move_to([x_admin, y_add_fin, 0]),
            pointer_del.animate.move_to([x_admin, y_del_fin, 0]),
            run_time=0.8
        )

        # [Step E] 모든 점 합류 (최종 위치)
        self.play(
            pointer.animate.move_to([x_admin, y_final, 0]),
            pointer_del.animate.move_to([x_admin, y_final, 0]),
            run_time=0.8
        )
        
        # 3개의 점이 동시에 깜빡임
        self.play(
            Flash(pointer, color=RED, flash_radius=0.5),
            Flash(pointer_del, color=ORANGE, flash_radius=0.5),
            Flash(pointer_mod, color=YELLOW, flash_radius=0.5)
        )

        # [Step F] 최종 Self Call (저장 완료)
        # 3개의 점이 겹쳐서 같이 움직임
        p_final_1 = [x_admin + 0.45, y_final, 0]
        p_final_2 = [x_admin + 0.45, y_final - 0.5, 0]
        p_final_3 = [x_admin, y_final - 0.5, 0]
        p_final_4 = [x_admin, y_final - 0.75, 0]

        self.play(
            pointer.animate.move_to(p_final_1),
            pointer_del.animate.move_to(p_final_1),
            pointer_mod.animate.move_to(p_final_1),
            run_time=0.3
        )
        self.play(
            pointer.animate.move_to(p_final_2),
            pointer_del.animate.move_to(p_final_2),
            pointer_mod.animate.move_to(p_final_2),
            run_time=0.5
        )
        self.play(
            pointer.animate.move_to(p_final_3),
            pointer_del.animate.move_to(p_final_3),
            pointer_mod.animate.move_to(p_final_3),
            run_time=0.3
        )

        self.play(
            pointer.animate.move_to(p_final_4),
            pointer_del.animate.move_to(p_final_4),
            pointer_mod.animate.move_to(p_final_4),
            run_time=0.3
        )

        # 마무리
        self.play(
            FadeOut(pointer), 
            FadeOut(pointer_del), 
            FadeOut(pointer_mod)
        )