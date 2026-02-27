
### 🎯 Our goal

**The main goal of the EcoLogits Calculator is to raise awareness on the environmental impacts of LLM inference.**

The rapid evolution of generative AI is reshaping numerous industries and aspects of our daily lives. While these advancements offer some benefits, they also **pose substantial environmental challenges that cannot be overlooked**. Plus the issue of AI's environmental footprint has been mainly discussed at training stage but rarely at the inference stage. That is an issue because **inference impacts for large langauge models (LLMs) can largely overcome the training impacts when deployed at large scales**.

At **[CodeCarbon](https://codecarbon.io/) we are dedicated to understanding and mitigating the environmental impacts of generative AI** through rigorous research, innovative tools, and community engagement. Especially, in early 2024 we have launched an new open-source tool called [EcoLogits](https://github.com/mlco2/ecologits) that tracks the energy consumption and environmental footprint of using generative AI models through APIs.


### 🙋 FAQ

**How we assess the impacts of closed-source models?**

Environmental impacts are calculated based on model architecture and parameter count. For closed-source models, we lack transparency from providers, so we estimate parameter counts using available information. For GPT models, we based our estimates on leaked GPT-4 architecture and scaled parameters count for GPT-4-Turbo and GPT-4o based on pricing differences. For other proprietary models like Anthropic's Claude, we assume similar impacts for models released around the same time with similar performance on public benchmarks. Please note that these estimates are based on assumptions and may not be exact. Our methods are open-source and transparent so you can always see the hypotheses we use.

**Which generative AI models or providers are supported?**

To see the full list of **generative AI providers** currently supported by EcoLogits, see the following [documentation page](https://ecologits.ai/providers/). As of today we only support LLMs but we plan to add support for embeddings, image generation, multi-modal models and more. If you are interested don't hesitate to [join us](https://codecarbon.io/contact/) and accelerate our work!

**How to reduce AI environmental impacts?**

* Look at **indirect impacts** of your project. Does the finality of your project is impacting negatively the environment?
* **Be frugal** and question your usage or need of AI
    * Do you really need AI to solve your problem?
    * Do you really need GenAI to solve your problem? (you can read this [paper](https://aclanthology.org/2023.emnlp-industry.39.pdf))
    * Use small and specialized models to solve your problem.
    * Evaluate before, during and after the development of your project the environmental impacts with tools like 🌱 [EcoLogits](https://github.com/mlco2/ecologits) or [CodeCarbon](https://github.com/mlco2/codecarbon) (see [more tools](https://github.com/samuelrince/awesome-green-ai))
    * Restrict the use case and limit the usage of your tool or feature to the desired purpose.
* Do NOT buy new GPUs / hardware
    * Hardware manufacturing for data centers is around 50% of the impact.
* Use cloud instances that are located in low emissions / high energy efficiency data centers (see [electricitymaps.com](https://app.electricitymaps.com/map))
* Optimize your models for production
    * Quantize your models.
    * Use inference optimization tricks.
    * Prefer fine-tuning of small and existing models over generalist models.

**What is the difference between **EcoLogits** and [CodeCarbon](https://github.com/mlco2/codecarbon)?**

EcoLogits is focused on estimating the environmental impacts of generative AI (only LLMs for now) used **through API providers (such as OpenAI, Anthropic, Cloud APIs...)** whereas  CodeCarbon is more general tool to measure energy consumption and estimate GHG emissions measurement. If you deploy LLMs locally we encourage you to use CodeCarbon to get real numbers of your energy consumption.


### 🤗 Contributing

We are eager to get feedback from the community, don't hesitate to engage the discussion with us on this [GitHub thread](https://github.com/mlco2/ecologits/discussions/45) or message us on [LinkedIn](https://www.linkedin.com/company/ecologits/).

We also welcome any open-source contributions on 🌱 **[EcoLogits](https://github.com/mlco2/ecologits)** or on 🧮 **EcoLogits Calculator**.


### ⚖️ License

<p xmlns:cc="http://creativecommons.org/ns#" >
  This work is licensed under
  <a href="https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">
    CC BY-SA 4.0
  </a>
</p>

### 🙌 Acknowledgement

We thank [Data For Good](https://dataforgood.fr/) and [Boavizta](https://boavizta.org/en) for supporting the development of this project. Their contributions of tools, best practices, and expertise in environmental impact assessment have been invaluable.


### 🤝 Contact

For general question on the project, please use the [GitHub thread](https://github.com/mlco2/ecologits/discussions/45).
Otherwise you can reach out on our [Discord channel](https://discord.gg/GS9js2XkJR).
