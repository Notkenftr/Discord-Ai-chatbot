


#### B1 Tạo bot
- Truy cập: https://discord.com/developers/applications
- Ở phần góc có cái nút New Application
- Bấm vào nhập name tuỳ bạn
#### B2 Lấy Token
- Vào phần bot ( thanh bên trái )
- Bấm vào Reset token
- Nhập mật khẩu vào
- Copy token
- Truy cập `Chatbotconfig.yml`
- Dán token vào
#### B3 Tạo api key gemini
- Truy cập: https://aistudio.google.com/prompts/new_chat
- Ở góc trái có nút get api key
- Tạo 1 api key copy và truy cập Chatbotconfig.yml sau đó dán vào
#### B4 Edit system_instruction.yml
```html
Data:
  system_instruction: "chat bot sử dụng tiếng việt"

bạn có thể viết thêm như cách bot chat, hỗ trợ về việc gì, sử dụng ngôn ngữ gì

Data:
  system_instruction: "chat bot sử dụng tiếng việt, hỗ trợ về minecraft"
```

#### B5 Cài đặt và chạy bot
- Sử dụng `pip install -r requirements.txt`
- Chờ tới khi hoàn tất!
- sau đó sử dụng `py main.py` hoặc `python main.py`
