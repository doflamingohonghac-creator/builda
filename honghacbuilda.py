from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Rectangle, Line
from kivy.core.window import Window
from kivy.clock import Clock
import os, subprocess, math, time
from PIL import Image

GAME_DIR = "/data/data/com.hortor.juliancysj/files/hsj/Cache/PaintCache/"
MOD_FOLDER = "/storage/emulated/0/mod/"
TEMP_FILE = "/storage/emulated/0/Download/current_layer.raw"

class NutNeon(Button):
    def __init__(self, bg_color=(0.1, 0.1, 0.2, 0.8), border_color=(0, 1, 1, 1), **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.markup = True
        self.bold = True
        self.c_bg = bg_color
        self.c_border = border_color
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.c_bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[5])
            Color(*self.c_border)
            Line(rounded_rectangle=(self.x, self.y, self.width, self.height, 5), width=1.1)

class LongBuildaApp(App):
    def build(self):
        self.path_mod = ""
        self.target_path = ""
        self.game_res = 0 
        self.clean_raw_data = None 
        self.paste_count = 0
        self.config_data = {"zoom": 100, "off_x": 0, "off_y": 0, "rotation": 0}
        self.fps_label_text = "FPS: --"

        self.root_container = FloatLayout()

        with self.root_container.canvas.before:
            Color(0.01, 0.01, 0.02, 1)
            Rectangle(pos=(0,0), size=Window.size)
        if os.path.exists('background.jpg'):
            bg_image = KivyImage(source='background.jpg', allow_stretch=True, keep_ratio=False, size_hint=(1, 1))
            bg_image.color = (0.5, 0.5, 0.5, 1)
            self.root_container.add_widget(bg_image)

        self.main_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        self.header = BoxLayout(orientation='vertical', size_hint_y=0.12, padding=[0, 10])
        self.header.add_widget(Label(text="[b][color=00ffff]HONGHAC BUILDA[/color][/b]", markup=True, font_size='24sp', halign='center'))
        self.header.add_widget(Label(text="[color=ffffff]Tải tool free tại https://konect.gg/hacnewsgame - discord : honghac.[color=ff0000[/color][/color]", markup=True, font_size='13sp', halign='center'))
        self.main_layout.add_widget(self.header)

        self.view_zone = FloatLayout(size_hint_y=0.53)
        with self.view_zone.canvas.before:
            self.frame_color = Color(0, 0, 0, 1) 
            self.frame_bg = Rectangle(pos=(0,0), size=(0,0))
        with self.view_zone.canvas.after:
            self.line_color = Color(0, 1, 1, 0)
            self.frame_line = Line(rectangle=(0, 0, 0, 0), width=2)
        self.img_display = KivyImage(source='', allow_stretch=True, keep_ratio=True, opacity=0, color=(1, 1, 1, 1))
        self.view_zone.add_widget(self.img_display)
        
        # Info panel
        self.info_label = Label(
            text="",
            markup=True,
            size_hint=(None, None),
            size=(220, 70),
            pos_hint={'x': 0.02, 'top': 0.98},
            font_size='11sp',
            halign='left',
            valign='top',
            color=(1, 1, 0, 0.9)
        )
        self.info_label.bind(size=lambda s, v: setattr(s, 'text_size', v))
        self.view_zone.add_widget(self.info_label)
        
        # FPS counter
        self.fps_label = Label(
            text="[b]FPS: --[/b]",
            markup=True,
            size_hint=(None, None),
            size=(100, 30),
            pos_hint={'right': 0.98, 'top': 0.98},
            font_size='12sp',
            halign='right',
            valign='top',
            color=(0, 1, 0, 0.9)
        )
        self.fps_label.bind(size=lambda s, v: setattr(s, 'text_size', v))
        self.view_zone.add_widget(self.fps_label)
        
        self.main_layout.add_widget(self.view_zone)

        # Rotation Panel
        self.rotation_panel = BoxLayout(orientation='horizontal', size_hint_y=0.08, padding=[15, 5], spacing=10)
        rotation_label = Label(text="[b]XOAY:[/b]", markup=True, size_hint_x=0.15, font_size='14sp')
        self.rotation_slider = Slider(min=0, max=360, value=0, step=1, size_hint_x=0.6, cursor_size=(20, 20))
        self.rotation_value_label = Label(text="[color=ffff00][b]0°[/b][/color]", markup=True, size_hint_x=0.15, font_size='16sp')
        reset_btn = NutNeon(text="RESET", size_hint_x=0.1, bg_color=(0.5, 0.1, 0.1, 0.8), border_color=(1, 0.3, 0.3, 1))
        self.rotation_slider.bind(value=self.on_rotation_change)
        reset_btn.bind(on_press=self.on_reset_all)
        self.rotation_panel.add_widget(rotation_label)
        self.rotation_panel.add_widget(self.rotation_slider)
        self.rotation_panel.add_widget(self.rotation_value_label)
        self.rotation_panel.add_widget(reset_btn)
        self.main_layout.add_widget(self.rotation_panel)

        self.msg_bar = FloatLayout(size_hint_y=0.1)
        with self.msg_bar.canvas.before:
            Color(0, 0, 0, 1) 
            Rectangle(pos=self.msg_bar.pos, size=self.msg_bar.size)
            Color(1, 1, 0, 0.8) 
            Line(points=[0, self.msg_bar.top, Window.width, self.msg_bar.top], width=1.2)
        self.main_msg = Label(text="[color=ffff00][b]HÃY BẤM 'QUÉT LAYER' ĐỂ BẮT ĐẦU[/b][/color]", markup=True, halign='center', valign='middle', font_size='14sp', bold=True, size_hint=(0.95, 0.95), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.main_msg.bind(size=lambda s, v: setattr(s, 'text_size', v))
        self.msg_bar.add_widget(self.main_msg)
        self.main_layout.add_widget(self.msg_bar)

        self.btn_panel = GridLayout(cols=3, spacing=5, padding=8, size_hint_y=0.25)
        btns = [("QUÉT LAYER", "scan", (0, 0.3, 0.6, 1), (0, 0.8, 1, 1)), ("LÊN", "w", (0.1, 0.1, 0.15, 0.8), (0.5, 0.5, 0.5, 1)), ("CHỌN ẢNH", "pick", (0, 0.4, 0.2, 1), (0, 1, 0.5, 1)), ("TRÁI", "a", (0.1, 0.1, 0.15, 0.8), (0.5, 0.5, 0.5, 1)), ("DÁN NGAY", "exec", (0.6, 0.1, 0.1, 1), (1, 0.2, 0.2, 1)), ("PHẢI", "d", (0.1, 0.1, 0.15, 0.8), (0.5, 0.5, 0.5, 1)), ("THU NHỎ", "-", (0.2, 0.2, 0.2, 0.8), (0.8, 0.8, 0, 1)), ("XUỐNG", "s", (0.1, 0.1, 0.15, 0.8), (0.5, 0.5, 0.5, 1)), ("PHÓNG TO", "+", (0.2, 0.2, 0.2, 0.8), (0.8, 0.8, 0, 1))]
        for t, cmd, bg, bd in btns:
            b = NutNeon(text=t, bg_color=bg, border_color=bd)
            if cmd == "scan": b.bind(on_press=self.on_scan)
            elif cmd == "pick": b.bind(on_press=self.on_pick)
            elif cmd == "exec": b.bind(on_press=self.on_execute)
            else: b.bind(on_press=lambda x, c=cmd: self.on_adjust(c))
            self.btn_panel.add_widget(b)

        self.main_layout.add_widget(self.btn_panel)
        self.root_container.add_widget(self.main_layout)
        self.view_zone.bind(size=self._sync, pos=self._sync)
        Window.bind(on_key_down=self._on_keyboard)
        Window.bind(on_mouse_scroll=self._on_mouse_scroll)
        Clock.schedule_interval(self._update_fps, 1.0)  # Update FPS mỗi giây
        Clock.schedule_once(self.show_welcome_popup, 0.5)
        return self.root_container

    def on_pause(self):
        # Giữ app trong RAM khi đổi tab ở Android
        return True

    def on_resume(self):
        # Callback khi app quay lại
        pass

    def show_welcome_popup(self, *args):
        content = BoxLayout(orientation='vertical', padding=20, spacing=15)
        content.add_widget(Label(text="Tool mod này hoàn toàn [b][color=00ff00]FREE[/color][/b],\ncó thể tải nó tại telegram:\n[color=00ffff]@freetoolmod[/color]", markup=True, halign='center', font_size='16sp'))
        btn = NutNeon(text="TÔI ĐÃ HIỂU", size_hint=(0.6, 0.3), pos_hint={'center_x': 0.5})
        content.add_widget(btn)
        self.welcome_pop = Popup(title="THÔNG BÁO", content=content, size_hint=(0.85, 0.4), auto_dismiss=False)
        btn.bind(on_press=self.welcome_pop.dismiss)
        self.welcome_pop.open()

    def _sync(self, *args):
        if self.game_res <= 0: return
        side = min(self.view_zone.width * 0.85, self.view_zone.height * 0.85)
        px, py = self.view_zone.center_x - side/2, self.view_zone.center_y - side/2
        self.frame_bg.size = (side, side)
        self.frame_bg.pos = (px, py)
        self.frame_line.rectangle = (px, py, side, side)
        self._refresh_img()

    def _refresh_img(self):
        if not self.img_display.source or self.game_res <= 0: return
        self.img_display.opacity = 1
        if self.img_display.texture:
            self.img_display.texture.min_filter = 'nearest'
            self.img_display.texture.mag_filter = 'nearest'
        ratio = self.frame_bg.size[0] / self.game_res
        zoom = self.config_data['zoom'] / 100
        dw = self.frame_bg.size[0] * zoom
        try:
            with Image.open(self.path_mod) as m:
                dh = dw * (m.height / m.width)
        except: dh = dw
        self.img_display.size_hint = (None, None)
        self.img_display.size = (dw, dh)
        self.img_display.center_x = self.frame_bg.pos[0] + (self.frame_bg.size[0]/2) + (self.config_data['off_x'] * ratio)
        self.img_display.center_y = self.frame_bg.pos[1] + (self.frame_bg.size[1]/2) - (self.config_data['off_y'] * ratio)

    def _update_info(self):
        if self.path_mod and self.game_res > 0:
            try:
                with Image.open(self.path_mod) as img:
                    info = f"[b]Ảnh:[/b] {img.width}x{img.height}\n"
                    info += f"[b]Layer:[/b] {self.game_res}x{self.game_res}\n"
                    info += f"[b]Zoom:[/b] {self.config_data['zoom']}% | [b]Xoay:[/b] {self.config_data['rotation']}°"
                    self.info_label.text = info
            except:
                pass
        else:
            self.info_label.text = ""

    def _update_fps(self, dt):
        from kivy.clock import Clock
        fps = Clock.get_fps()
        self.fps_label.text = f"[b]FPS: {fps:.0f}[/b]"

    def on_scan(self, *args):
        cmd = f"su -c 'ls -lt {GAME_DIR}'"
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if not res.stdout or "No such file" in res.stderr:
            self.main_msg.text = "[color=ff3333][b]LỖI: KHÔNG TÌM THẤY DỮ LIỆU GAME![/b][/color]\n[size=12sp]Hãy vào game tạo khung -> Tô đen kín -> Quay lại quét.[/size]"
            return
        lines = res.stdout.split('\n')[1:]
        hop_le = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 8:
                size, name = int(parts[4]), parts[-1]
                if size > 50000 and name.endswith('.dat'):
                    hop_le.append((name, size))
        if not hop_le:
            self.main_msg.text = "[color=ff3333][b]KHÔNG TÌM THẤY KHUNG VẼ![/b][/color]\n[size=12sp]Vui lòng tô màu kín khung hình trong game rồi thử lại.[/size]"
            return
        content = BoxLayout(orientation='vertical', padding=10, spacing=8)
        scroll = ScrollView()
        list_ui = GridLayout(cols=1, spacing=10, size_hint_y=None)
        list_ui.bind(minimum_height=list_ui.setter('height'))
        for name, size in hop_le:
            res_val = "1024x1024" if size > 4000000 else "512x512"
            btn = NutNeon(text=f"BẢN VẼ: {name} ({res_val})", size_hint_y=None, height=110)
            btn.bind(on_release=lambda x, n=name: self.on_select_layer(n))
            list_ui.add_widget(btn)
        scroll.add_widget(list_ui)
        content.add_widget(scroll)
        self.pop = Popup(title="DANH SÁCH KHUNG", content=content, size_hint=(0.9, 0.8))
        self.pop.open()

    def on_select_layer(self, name):
        self.target_path = os.path.join(GAME_DIR, name)
        try:
            subprocess.run(f"su -c 'cp -f {self.target_path} {TEMP_FILE}'", shell=True)
            with open(TEMP_FILE, "rb") as f: self.clean_raw_data = f.read()
            self.game_res = int(math.sqrt(len(self.clean_raw_data) / 4))
            self.paste_count = 0
            self.frame_color.a, self.line_color.a = 1.0, 0.8 
            self._sync()
            self.main_msg.text = f"[color=00ff00]ĐÃ CHỌN: {name}[/color]\n[color=ffffff]BƯỚC TIẾP: BẤM 'CHỌN ẢNH'[/color]"
            self.pop.dismiss()
        except: self.main_msg.text = "[color=ff3333]LỖI KHÔNG ĐỌC ĐƯỢC FILE![/color]"

    def on_pick(self, instance):
        if self.game_res <= 0:
            self.main_msg.text = "[color=ff3333][b]CẢNH BÁO: HÃY QUÉT LAYER TRƯỚC![/b][/color]"
            return
        if not os.path.exists(MOD_FOLDER):
            self.main_msg.text = "[color=ff3333][b]LỖI: THƯ MỤC /mod/ KHÔNG TỒN TẠI![/b][/color]"
            return
        files = [f for f in os.listdir(MOD_FOLDER) if f.lower().endswith(('.png', '.jpg'))]
        if not files:
            self.main_msg.text = "[color=ff3333][b]LỖI: THƯ MỤC /mod/ ĐANG TRỐNG![/b][/color]\n[size=12sp]Hãy chép ảnh vào thư mục mod rồi thử lại.[/size]"
            return
        content = BoxLayout(orientation='vertical', padding=10, spacing=5)
        scroll = ScrollView()
        list_ui = GridLayout(cols=1, spacing=10, size_hint_y=None)
        list_ui.bind(minimum_height=list_ui.setter('height'))
        for f in files:
            btn = NutNeon(text=f, size_hint_y=None, height=110, border_color=(0,1,0.5,1))
            btn.bind(on_release=lambda x, p=os.path.join(MOD_FOLDER, f): self.on_apply_img(p))
            list_ui.add_widget(btn)
        scroll.add_widget(list_ui)
        content.add_widget(scroll)
        self.pop_img = Popup(title="CHỌN ẢNH MOD", content=content, size_hint=(0.9, 0.8))
        self.pop_img.open()

    def on_apply_img(self, path):
        self.path_mod, self.img_display.source = path, path
        self.img_display.reload()
        self._refresh_img()
        self._update_info()
        self.pop_img.dismiss()
        self.main_msg.text = "[color=ffff00][b]ĐÃ TẢI ẢNH.[/b] Chỉnh vị trí rồi bấm 'DÁN NGAY'[/color]"

    def on_adjust(self, cmd):
        if self.game_res <= 0: return
        buoc = 10 if cmd in 'wsad' else 5
        if cmd == '+': self.config_data['zoom'] += buoc
        elif cmd == '-': self.config_data['zoom'] = max(5, self.config_data['zoom'] - buoc)
        elif cmd == 'w': self.config_data['off_y'] -= buoc
        elif cmd == 's': self.config_data['off_y'] += buoc
        elif cmd == 'a': self.config_data['off_x'] -= buoc
        elif cmd == 'd': self.config_data['off_x'] += buoc
        self._refresh_img()

    def on_rotation_change(self, instance, value):
        self.config_data['rotation'] = int(value)
        self.rotation_value_label.text = f"[color=ffff00][b]{int(value)}°[/b][/color]"
        self._update_info()

    def on_reset_all(self, instance):
        if self.game_res <= 0:
            return
        self.config_data = {"zoom": 100, "off_x": 0, "off_y": 0, "rotation": 0}
        self.rotation_slider.value = 0
        self._refresh_img()
        self._update_info()
        self.main_msg.text = "[color=00ff00][b]ĐÃ RESET VỀ MẶC ĐỊNH![/b][/color]"

    def _on_keyboard(self, window, key, scancode, codepoint, modifier):
        if codepoint == "r":
            self.on_reset_all(None)
        elif key == 32 and self.path_mod and self.clean_raw_data:
            self.on_execute(None)
        elif codepoint == "w":
            self.on_adjust("w")
        elif codepoint == "s":
            self.on_adjust("s")
        elif codepoint == "a":
            self.on_adjust("a")
        elif codepoint == "d":
            self.on_adjust("d")

    def _on_mouse_scroll(self, window, x, y, dx, dy):
        if 'ctrl' in Window.modifiers and self.game_res > 0:
            if dy > 0:
                self.on_adjust('+')
            else:
                self.on_adjust('-')
            self._update_info()

    def on_execute(self, instance):
        if not self.path_mod or not self.clean_raw_data: return
        try:
            canvas = Image.frombytes("RGBA", (self.game_res, self.game_res), self.clean_raw_data).transpose(Image.FLIP_TOP_BOTTOM)
            mod_img = Image.open(self.path_mod).convert("RGBA")
            if mod_img.getbbox(): mod_img = mod_img.crop(mod_img.getbbox())
            # Apply rotation
            if self.config_data['rotation'] != 0:
                mod_img = mod_img.rotate(-self.config_data['rotation'], expand=True, resample=Image.Resampling.BILINEAR)
            zoom = self.config_data['zoom'] / 100
            nw, nh = int(self.game_res * zoom), int(mod_img.size[1] * (int(self.game_res * zoom) / mod_img.size[0]))
            mod_img = mod_img.resize((nw, nh), Image.Resampling.NEAREST)
            canvas.paste(mod_img, ((self.game_res - nw) // 2 + self.config_data['off_x'], (self.game_res - nh) // 2 + self.config_data['off_y']), mod_img)
            with open(TEMP_FILE, "wb") as f: f.write(canvas.transpose(Image.FLIP_TOP_BOTTOM).tobytes())
            subprocess.run(f"su -c 'cp -f {TEMP_FILE} {self.target_path} && sync'", shell=True)
            self.paste_count += 1
            if self.paste_count == 1:
                self.main_msg.text = "[color=00ff00][b]ĐÃ DÁN XONG![/b][/color]\n[size=12sp]Vào game bấm [b]↩️ Quay lại[/b] để hiện ảnh.[/size]"
            else:
                self.main_msg.text = "[color=00ff00][b]ĐÃ CẬP NHẬT![/b][/color]\n[size=12sp]Vào game bấm [b]↪️ Làm lại[/b] rồi bấm [b]↩️ Quay lại[/b] để cập nhật.[/size]"
        except Exception as e: self.main_msg.text = f"[color=ff3333]LỖI: {str(e)[:15]}[/color]"

if __name__ == '__main__':
    LongBuildaApp().run()
