# Flutter Mobile App Development Guide with VS Code, GitHub Copilot & Claude

This guide explains how to set up Flutter mobile app development using Visual Studio Code, GitHub Copilot, and Claude Opus 4.5 on a Google Cloud Platform (GCP) IaaS Machine.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setting Up GCP VM for Development](#setting-up-gcp-vm-for-development)
3. [Installing Flutter on GCP VM](#installing-flutter-on-gcp-vm)
4. [Setting Up VS Code with Remote Development](#setting-up-vs-code-with-remote-development)
5. [Configuring GitHub Copilot](#configuring-github-copilot)
6. [Using Claude Opus 4.5 for Development](#using-claude-opus-45-for-development)
7. [Connecting Flutter App to Food Management Backend](#connecting-flutter-app-to-food-management-backend)
8. [Sample Flutter Project Structure](#sample-flutter-project-structure)
9. [Development Workflow](#development-workflow)
10. [Testing on Physical Devices](#testing-on-physical-devices)

---

## Prerequisites

Before starting, ensure you have:
- A Google Cloud Platform account with billing enabled
- A GitHub account with GitHub Copilot subscription
- Access to Claude (via Anthropic API or Claude Desktop)
- Basic knowledge of Dart and Flutter

---

## Setting Up GCP VM for Development

### Step 1: Create a GCP Compute Engine Instance

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **Compute Engine** > **VM instances**
3. Click **Create Instance**

**Recommended Configuration:**
```
Name: flutter-dev-vm
Region: Choose closest to your location
Machine type: e2-standard-4 (4 vCPU, 16 GB memory) or higher
Boot disk:
  - OS: Ubuntu 22.04 LTS
  - Size: 100 GB SSD
Firewall: Allow HTTP and HTTPS traffic
```

### Step 2: Configure SSH Access

```bash
# Generate SSH key if not already done
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Add your public key to GCP VM metadata
# Go to Compute Engine > Metadata > SSH Keys
# Add your public key (~/.ssh/id_rsa.pub content)
```

### Step 3: Connect to Your VM

```bash
# Connect using gcloud CLI
gcloud compute ssh flutter-dev-vm --zone=YOUR_ZONE

# Or use SSH directly
ssh -i ~/.ssh/id_rsa username@EXTERNAL_IP
```

---

## Installing Flutter on GCP VM

### Step 1: Update System and Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required dependencies
sudo apt install -y curl git unzip xz-utils zip libglu1-mesa \
  clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev \
  libstdc++-12-dev

# Install Chrome for web development (optional)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt --fix-broken install -y
```

### Step 2: Install Flutter SDK

```bash
# Download Flutter SDK
cd ~
git clone https://github.com/flutter/flutter.git -b stable

# Add Flutter to PATH
echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
flutter --version
flutter doctor
```

### Step 3: Install Android SDK (for Android Development)

```bash
# Download Android Command Line Tools
mkdir -p ~/Android/cmdline-tools
cd ~/Android/cmdline-tools
wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip
unzip commandlinetools-linux-9477386_latest.zip
mv cmdline-tools latest

# Add to PATH
echo 'export ANDROID_HOME="$HOME/Android"' >> ~/.bashrc
echo 'export PATH="$PATH:$ANDROID_HOME/cmdline-tools/latest/bin"' >> ~/.bashrc
echo 'export PATH="$PATH:$ANDROID_HOME/platform-tools"' >> ~/.bashrc
source ~/.bashrc

# Accept licenses and install SDK components
yes | sdkmanager --licenses
sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"

# Run Flutter doctor to verify
flutter doctor
```

---

## Setting Up VS Code with Remote Development

### Step 1: Install VS Code on Local Machine

Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com/)

### Step 2: Install Required Extensions

Install these VS Code extensions:
- **Remote - SSH** (by Microsoft)
- **Flutter** (by Dart Code)
- **Dart** (by Dart Code)
- **GitHub Copilot** (by GitHub)
- **GitHub Copilot Chat** (by GitHub)

### Step 3: Connect to GCP VM via SSH

1. Press `F1` or `Ctrl+Shift+P`
2. Type "Remote-SSH: Connect to Host"
3. Enter: `username@EXTERNAL_IP`
4. Select Linux when prompted
5. Wait for VS Code Server to install

### Step 4: Install Flutter Extensions on Remote

Once connected, install Flutter and Dart extensions on the remote server:
1. Go to Extensions view
2. Search for "Flutter"
3. Click "Install in SSH: your-vm"

---

## Configuring GitHub Copilot

### Step 1: Sign in to GitHub Copilot

1. Open VS Code
2. Click on the GitHub Copilot icon in the sidebar
3. Sign in with your GitHub account
4. Authorize VS Code to use Copilot

### Step 2: Configure Copilot Settings

Open VS Code settings (`Ctrl+,`) and add:

```json
{
  "github.copilot.enable": {
    "*": true,
    "dart": true,
    "yaml": true,
    "markdown": true
  },
  "github.copilot.advanced": {
    "inlineSuggestCount": 3
  }
}
```

### Step 3: Using Copilot Effectively

**Inline Suggestions:**
- Start typing and Copilot will suggest code
- Press `Tab` to accept suggestions
- Press `Alt+]` to see next suggestion
- Press `Alt+[` to see previous suggestion

**Copilot Chat:**
- Open Copilot Chat panel (`Ctrl+Shift+I`)
- Ask questions like:
  - "Create a Flutter widget for displaying food menu items"
  - "How do I call REST API from Flutter?"
  - "Generate a model class for Order from this JSON"

---

## Using Claude Opus 4.5 for Development

### Option 1: Claude Desktop App

1. Download Claude Desktop from [claude.ai](https://claude.ai/)
2. Sign in with your Anthropic account
3. Use Claude for:
   - Code review and optimization
   - Architecture decisions
   - Debugging complex issues
   - Learning Flutter concepts

### Option 2: Claude API Integration

Create a helper script to interact with Claude API:

```python
# claude_helper.py
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")

def ask_claude(prompt):
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# Example usage
response = ask_claude("Create a Flutter widget for a food menu card with image, title, price")
print(response)
```

### Option 3: Using Claude with VS Code Extension

1. Install "Claude Dev" or similar Claude-integrated extension
2. Configure your Anthropic API key
3. Use Claude alongside Copilot for complex tasks

### Best Practices for Using AI Assistants

| Task | Best Tool |
|------|-----------|
| Quick code completion | GitHub Copilot |
| Complex logic design | Claude Opus 4.5 |
| API integration patterns | Claude or Copilot Chat |
| UI widget creation | Copilot with context |
| Debugging | Claude with error context |
| Code review | Claude Opus 4.5 |

---

## Connecting Flutter App to Food Management Backend

This repository contains a Flask backend for food management. Here's how to connect a Flutter mobile app:

### Step 1: API Base Configuration

```dart
// lib/config/api_config.dart
class ApiConfig {
  // For development (replace with your GCP VM IP)
  static const String baseUrl = 'https://YOUR_GCP_VM_IP:4009';
  
  // API endpoints matching Flask backend
  static const String login = '/login';
  static const String dashboard = '/dashboard';
  static const String menuItems = '/api/menu_items';
  static const String orders = '/orders';
  static const String createOrder = '/orders/create';
  static const String customers = '/api/customers/search';
}
```

### Step 2: API Service

```dart
// lib/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';

class ApiService {
  String? _sessionCookie;

  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.login}'),
      body: {
        'username': username,
        'password': password,
      },
    );

    // Store session cookie
    _sessionCookie = response.headers['set-cookie'];
    
    return json.decode(response.body);
  }

  Future<List<dynamic>> getMenuItems() async {
    final response = await http.get(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.menuItems}'),
      headers: {
        'Cookie': _sessionCookie ?? '',
      },
    );

    final data = json.decode(response.body);
    return data['menu_items'] ?? [];
  }

  Future<Map<String, dynamic>> createOrder({
    required String clientName,
    required String clientMobile,
    required List<Map<String, dynamic>> items,
    required DateTime deliveryDate,
    String? notes,
  }) async {
    final response = await http.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.createOrder}'),
      headers: {
        'Cookie': _sessionCookie ?? '',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'client_name': clientName,
        'client_mobile': clientMobile,
        'items': items,
        'delivery_date': deliveryDate.toIso8601String(),
        'notes': notes,
      }),
    );

    return json.decode(response.body);
  }
}
```

### Step 3: Model Classes

```dart
// lib/models/menu_item.dart
class MenuItem {
  final int id;
  final String name;
  final String? arabicName;
  final String? description;
  final double price;
  final String? categoryName;
  final String? image;
  final bool isAvailable;

  MenuItem({
    required this.id,
    required this.name,
    this.arabicName,
    this.description,
    required this.price,
    this.categoryName,
    this.image,
    required this.isAvailable,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    return MenuItem(
      id: json['id'],
      name: json['name'],
      arabicName: json['arabic_name'],
      description: json['description'],
      price: (json['price'] as num).toDouble(),
      categoryName: json['category_name'],
      image: json['image'],
      isAvailable: json['is_available'] ?? true,
    );
  }
}
```

---

## Sample Flutter Project Structure

```
food_management_mobile/
├── lib/
│   ├── main.dart
│   ├── config/
│   │   ├── api_config.dart
│   │   └── theme_config.dart
│   ├── models/
│   │   ├── menu_item.dart
│   │   ├── order.dart
│   │   ├── client.dart
│   │   └── user.dart
│   ├── services/
│   │   ├── api_service.dart
│   │   ├── auth_service.dart
│   │   └── notification_service.dart
│   ├── providers/
│   │   ├── auth_provider.dart
│   │   ├── cart_provider.dart
│   │   └── order_provider.dart
│   ├── screens/
│   │   ├── login_screen.dart
│   │   ├── dashboard_screen.dart
│   │   ├── menu/
│   │   │   ├── menu_list_screen.dart
│   │   │   └── menu_item_detail_screen.dart
│   │   ├── orders/
│   │   │   ├── orders_list_screen.dart
│   │   │   ├── create_order_screen.dart
│   │   │   └── order_detail_screen.dart
│   │   └── settings/
│   │       └── settings_screen.dart
│   └── widgets/
│       ├── menu_item_card.dart
│       ├── order_card.dart
│       ├── cart_drawer.dart
│       └── common/
│           ├── loading_indicator.dart
│           └── error_widget.dart
├── assets/
│   ├── images/
│   └── fonts/
├── test/
├── pubspec.yaml
└── README.md
```

### Create New Flutter Project

```bash
# Create Flutter project
flutter create food_management_mobile
cd food_management_mobile

# Add dependencies
flutter pub add http provider shared_preferences intl
flutter pub add --dev flutter_lints

# Run the app
flutter run
```

---

## Development Workflow

### Daily Development Process

1. **Start your GCP VM** (if stopped)
   ```bash
   gcloud compute instances start flutter-dev-vm --zone=YOUR_ZONE
   ```

2. **Connect VS Code to VM via SSH**

3. **Open your Flutter project**

4. **Use GitHub Copilot for coding**
   - Let Copilot suggest code as you type
   - Use Copilot Chat for complex questions

5. **Use Claude for architecture decisions**
   - Discuss complex features
   - Get code review
   - Debug issues

6. **Test on connected device or emulator**

7. **Commit changes to GitHub**

### Using Both AI Assistants Together

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Flow                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Plan Feature ──► Ask Claude for architecture advice     │
│           │                                                 │
│           ▼                                                 │
│  2. Write Code ──► Use Copilot for inline suggestions      │
│           │                                                 │
│           ▼                                                 │
│  3. Complex Logic ──► Ask Copilot Chat or Claude           │
│           │                                                 │
│           ▼                                                 │
│  4. Review Code ──► Ask Claude to review your changes      │
│           │                                                 │
│           ▼                                                 │
│  5. Debug Issues ──► Copilot Chat for quick fixes          │
│                      Claude for complex debugging           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Testing on Physical Devices

### Option 1: Android Device via ADB over Network

```bash
# On your local machine with physical Android device connected
adb tcpip 5555
adb connect DEVICE_IP:5555

# Forward connection to GCP VM
ssh -R 5555:DEVICE_IP:5555 username@GCP_VM_IP

# On GCP VM
export ADB_SERVER_SOCKET=tcp:localhost:5555
flutter devices
flutter run
```

### Option 2: Use Firebase App Distribution

```bash
# Build APK
flutter build apk --release

# Upload to Firebase App Distribution
firebase appdistribution:distribute build/app/outputs/flutter-apk/app-release.apk \
  --app YOUR_FIREBASE_APP_ID \
  --groups "testers"
```

### Option 3: Use scrcpy for Screen Mirroring

```bash
# On local machine with device connected
scrcpy --tcpip=DEVICE_IP:5555

# This mirrors your phone screen while allowing ADB commands from VM
```

---

## Troubleshooting

### Common Issues

**Issue: Flutter doctor shows missing dependencies**
```bash
# Run flutter doctor with verbose output
flutter doctor -v

# Install missing dependencies
sudo apt install <missing-package>
```

**Issue: VS Code can't connect to remote**
- Check firewall rules on GCP
- Verify SSH key is added to VM metadata
- Try reconnecting

**Issue: Copilot not suggesting code**
- Ensure you're signed in to GitHub
- Check Copilot subscription status
- Restart VS Code

**Issue: Can't connect to Flask backend**
- Verify the Flask server is running
- Check GCP firewall allows port 4009
- Ensure HTTPS certificates are valid

---

## Resources

- [Flutter Documentation](https://flutter.dev/docs)
- [Dart Language Guide](https://dart.dev/guides)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Claude API Documentation](https://docs.anthropic.com/claude/reference)
- [GCP Compute Engine Documentation](https://cloud.google.com/compute/docs)

---

## Next Steps

1. Set up your GCP VM following this guide
2. Install Flutter and configure VS Code
3. Clone this repository to get the Flask backend
4. Create a new Flutter project for the mobile app
5. Connect the mobile app to the Flask API
6. Start building features using Copilot and Claude!

---

*This guide is part of the Food Management System project. The Flask backend provides REST APIs that can be consumed by the Flutter mobile app.*
