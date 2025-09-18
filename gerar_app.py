import os
import zipfile

# Estrutura do projeto
files = {
    "ativar_bot/pubspec.yaml": """name: ativar_bot
description: App para ativar scripts no Termux
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: ">=3.0.0 <4.0.0"

dependencies:
  flutter:
    sdk: flutter
  url_launcher: ^6.1.14

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0

flutter:
  uses-material-design: true
""",

    "ativar_bot/lib/main.dart": """import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ativar Bot Termux',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const BotPage(),
    );
  }
}

class BotPage extends StatefulWidget {
  const BotPage({super.key});

  @override
  State<BotPage> createState() => _BotPageState();
}

class _BotPageState extends State<BotPage> {
  final _controller = TextEditingController(text: "meu_bot.py");

  Future<void> runScript() async {
    final script = _controller.text.trim();
    if (script.isEmpty) return;

    final command = "python $script";
    final uri = Uri.parse("termux://$command");

    if (await canLaunchUrl(uri)) {
      await launchUrl(uri);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("⚠️ Termux não encontrado.")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Ativar Bot")),
      body: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(
                labelText: "Nome do script Python",
                hintText: "ex: bot.py",
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: runScript,
              icon: const Icon(Icons.play_arrow),
              label: const Text("Ativar Bot"),
            ),
          ],
        ),
      ),
    );
  }
}
"""
}

# Criar pastas e arquivos
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# Compactar em ZIP
zip_filename = "ativar_bot.zip"
with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
    for path in files.keys():
        zipf.write(path)

print(f"✅ Projeto gerado e compactado em {zip_filename}")