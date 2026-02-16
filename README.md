---
title: EcoLogits Calculator
emoji: 🧮
colorFrom: green
colorTo: indigo
sdk: streamlit
sdk_version: 1.53.1
app_file: app.py
pinned: true
license: cc-by-sa-4.0
---

# EcoLogits Calculator

<div align="center">
  <a href="https://ecologits.ai/">
    <img alt="EcoLogits" src="https://raw.githubusercontent.com/mlco2/ecologits-calculator/main/assets/logo.png" width="200" />
  </a>
  
  <br />
  
  **Measure the Environmental Impact of Generative AI**
  
  [![License](https://img.shields.io/badge/license-CC%20BY--SA%204.0-blue.svg)](LICENSE)
  [![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
  [![Streamlit](https://img.shields.io/badge/built%20with-streamlit-FF4B4B.svg)](https://streamlit.io/)

</div>

---

## 🌍 About

**EcoLogits Calculator** is an open-source interactive tool for estimating the **energy consumption** and **environmental footprint** of generative AI models. Developed by the non-profit [CodeCarbon](https://codecarbon.io/), this calculator helps individuals, researchers, and organizations understand and evaluate the sustainability of AI usage.

The calculator provides:
- **Energy consumption estimates** for AI model inference
- **Environmental impact assessments** including carbon emissions and water usage
- **Real-world scaling analysis** to understand the broader impact
- **Support for multiple AI providers and models**
- **Educational insights** into sustainable AI practices

## ✨ Features

- **🧮 Interactive Calculator**: Easily estimate environmental impacts by selecting a provider, model, and example usage
- **🤓 Expert Mode**: Advanced options for users who want granular control over calculations
- **🪙 Token Estimator**: Understand tokenization and estimate token counts for your inputs
- **📊 Visualization**: Interactive charts showing environmental equivalences and scaling projections
- **🌐 Multi-Provider Support**: Evaluate impacts across different AI providers and models
- **📖 Methodology Documentation**: Transparent, science-backed calculation methods
- **📱 Web-Based Interface**: No installation needed—access directly through the web

## 🚀 Quick Start

The Calculator is currently hosted on Hugging Face Spaces and can be accessed directly [here](https://huggingface.co/spaces/genai-impact/ecologits-calculator).

If you want to run the calculator locally, follow the instructions below.

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/mlco2/ecologits-calculator.git
cd ecologits-calculator

# Install dependencies using uv
uv sync

# Run the application
uv run streamlit run app.py
```

The calculator will open in your browser at `http://localhost:8501`

## 📚 How It Works
The basic workflow of the EcoLogits Calculator involves the following steps:
1. **Select Model**: Choose an AI provider and model from the available options
2. **Provide Input**: Enter example prompts or text that you want to evaluate
3. **View Results**: Instantly see energy consumption and environmental impact estimates
4. **Explore Equivalences**: Understand impacts in relatable terms (e.g., "equivalent to driving X km")
5. **Analyze Scaling**: See how impacts multiply when scaled to larger populations

### Key Metrics

- **Energy Consumption**: Measured in kWh per inference
- **Carbon Emissions**: Estimated CO₂ equivalent based on energy grid composition
- **Other Environmental Impacts**: Water usage, resource consumption, etc.
- **Scaling Analysis**: Projections for 1% of world population using the same prompt daily for one year


## 📖 Learning More

- **[Methodology](https://ecologits.ai/latest/methodology/)**: Detailed explanation of how environmental impacts are calculated
- **[EcoLogits Documentation](https://ecologits.ai/dev/reference/_ecologits/)**: Learn about the underlying EcoLogits library
- **[CodeCarbon](https://codecarbon.io/)**: Learn more about the organization behind this project

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to:
- Report bugs
- Suggest features
- Submit pull requests
- Set up your development environment

## 📜 License

This project is licensed under the [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1) License.

## 🙏 Support

If you find this tool helpful, please consider:
- ⭐ Starring this repository
- 💬 Sharing feedback and suggestions
- 🤝 Contributing to the project
- 💝 Supporting [CodeCarbon](https://codecarbon.io/) on their mission to make AI more sustainable

## 📬 Questions?

Have questions or feedback? Feel free to:
- Open an [issue](https://github.com/mlco2/ecologits-calculator/issues)
- Start a [discussion](https://github.com/mlco2/ecologits-calculator/discussions)
- Contact [CodeCarbon](https://codecarbon.io/)

---

<div align="center">
  <p>Developed with ❤️ by <a href="https://codecarbon.io/">CodeCarbon</a></p>
</div>