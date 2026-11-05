from manim import *

class StudyZoneArchitecture(Scene):
    def construct(self):
        # 1. [스타일 설정] 애플 블루프린트 테마
        # 진한 남색 배경으로 청사진 느낌 연출
        self.camera.background_color = "#001A33" 
        
        # 네온 스타일 색상 팔레트
        BLUE_NEON = "#00F0FF"
        WHITE_NEON = "#FFFFFF"
        YELLOW_NEON = "#FFD700"
        RED_NEON = "#FF4B4B"
        
        # 기본 도형 스타일 (투명도 있는 채우기 + 밝은 테두리)
        # corner_radius는 RoundedRectangle에서만 작동하므로 여기서 정의
        box_style = {
            "stroke_color": BLUE_NEON, 
            "stroke_width": 3, 
            "fill_color": BLUE_NEON, 
            "fill_opacity": 0.1,
            "corner_radius": 0.2 
        }

        # 2. [구성 요소 배치] 아키텍처 구조 잡기
        
        # (1) 제목
        title = Text("Event-Driven Architecture", font="Pretendard", font_size=40, color=WHITE_NEON)
        title.to_edge(UP, buff=0.5)
        
        # (2) 센서 시스템 (왼쪽) - Rectangle 대신 RoundedRectangle 사용
        sensor_box = RoundedRectangle(height=2, width=3, **box_style).to_edge(LEFT, buff=1)
        sensor_label = Text("Sensor System\n(IoT)", font="Pretendard", font_size=24, color=WHITE_NEON).move_to(sensor_box)
        
        # (3) 메인 서버 & 옵저버 패턴 (중앙)
        server_box = RoundedRectangle(height=4, width=5, **box_style).move_to(ORIGIN)
        server_label = Text("Main Server", font="Pretendard", font_size=28, color=WHITE_NEON).move_to(server_box).to_edge(UP, buff=2.5)
        
        # 옵저버 패턴 내부 구조
        observer_circle = Circle(radius=1.0, color=YELLOW_NEON, stroke_width=4).move_to(server_box)
        observer_text = Text("Observer\nPattern", font="Pretendard", font_size=20, color=YELLOW_NEON).move_to(observer_circle)

        # (4) 클라이언트 앱 (오른쪽 상단)
        client_box = RoundedRectangle(height=2, width=3, **box_style).to_edge(RIGHT, buff=1).shift(UP*1.5)
        client_label = Text("Client App\n(Student/Admin)", font="Pretendard", font_size=24, color=WHITE_NEON).move_to(client_box)

        # (5) 데이터베이스 (오른쪽 하단)
        db_box = RoundedRectangle(height=1.5, width=3, **box_style).to_edge(RIGHT, buff=1).shift(DOWN*1.5)
        db_label = Text("Database\n(MySQL)", font="Pretendard", font_size=24, color=WHITE_NEON).move_to(db_box)

        # 3. [애니메이션 시퀀스] 그리기 및 데이터 흐름

        # Scene 1: 구조 생성 (청사진이 그려지듯)
        self.play(Write(title), run_time=1)
        self.play(
            Create(sensor_box), Write(sensor_label),
            Create(server_box), Write(server_label),
            Create(client_box), Write(client_label),
            Create(db_box), Write(db_label),
            run_time=2
        )
        self.wait(0.5)

        # Scene 2: 센서 감지 이벤트 발생
        # 센서 박스가 깜빡거림
        self.play(sensor_box.animate.set_fill(RED_NEON, opacity=0.3), run_time=0.3)
        self.play(sensor_box.animate.set_fill(BLUE_NEON, opacity=0.1), run_time=0.3)
        
        event_text = Text("Event: Seat Occupied", font_size=18, color=RED_NEON).next_to(sensor_box, UP)
        self.play(FadeIn(event_text, shift=UP))

        # Scene 3: 데이터 전송 (센서 -> 서버)
        arrow1 = Arrow(sensor_box.get_right(), server_box.get_left(), color=WHITE_NEON, buff=0.1)
        self.play(GrowArrow(arrow1))
        
        # 데이터 패킷이 이동하는 효과
        packet1 = Dot(color=RED_NEON).move_to(sensor_box.get_right())
        self.play(MoveAlongPath(packet1, Line(sensor_box.get_right(), server_box.get_left())), run_time=0.8)
        self.remove(packet1)

        # Scene 4: 서버 내부 처리 (옵저버 패턴 작동)
        self.play(Create(observer_circle), Write(observer_text))
        self.play(Indicate(observer_circle, color=YELLOW_NEON, scale_factor=1.2)) # 강조 효과

        # Scene 5: 상태 전파 (서버 -> 클라이언트 & DB)
        # 동시에 퍼져나가는 화살표
        arrow_to_client = Arrow(server_box.get_right(), client_box.get_left(), color=YELLOW_NEON, buff=0.1)
        arrow_to_db = Arrow(server_box.get_right(), db_box.get_left(), color=YELLOW_NEON, buff=0.1)
        
        self.play(GrowArrow(arrow_to_client), GrowArrow(arrow_to_db))

        # 데이터 패킷이 동시에 날아감 (브로드캐스트)
        packet_c = Dot(color=YELLOW_NEON).move_to(server_box.get_right())
        packet_d = Dot(color=YELLOW_NEON).move_to(server_box.get_right())
        
        self.play(
            MoveAlongPath(packet_c, Line(server_box.get_right(), client_box.get_left())),
            MoveAlongPath(packet_d, Line(server_box.get_right(), db_box.get_left())),
            run_time=1
        )
        self.remove(packet_c, packet_d)

        # Scene 6: 반응 (UI 업데이트 & DB 저장)
        # 클라이언트와 DB 박스가 동시에 반응
        ui_update_text = Text("UI Update!", font_size=16, color=YELLOW_NEON).next_to(client_box, UP)
        db_save_text = Text("Commit", font_size=16, color=YELLOW_NEON).next_to(db_box, DOWN)

        self.play(
            client_box.animate.set_fill(YELLOW_NEON, opacity=0.3),
            db_box.animate.set_fill(YELLOW_NEON, opacity=0.3),
            FadeIn(ui_update_text, shift=UP),
            FadeIn(db_save_text, shift=DOWN)
        )
        self.play(
            client_box.animate.set_fill(BLUE_NEON, opacity=0.1),
            db_box.animate.set_fill(BLUE_NEON, opacity=0.1)
        )

        self.wait(2)
        
        # 마무리: 전체 페이드 아웃
        self.play(FadeOut(Group(*self.mobjects)))