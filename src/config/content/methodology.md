
### 📖 Methodology

We have developed a methodology to **estimate the energy consumption and environmental impacts for an LLM inference** based on request parameters and hypotheses on the data center location, the hardware used, the model architecture and more.

In this section we will only cover the principles of the methodology related to the 🧮 **EcoLogits Calculator**. If you wish to learn more on the environmental impacts modeling of an LLM request checkout the 🌱 [EcoLogits documentation page](https://ecologits.ai/methodology/).

#### Modeling impacts of an LLM request

The environmental impacts of an LLM inference are split into the **usage impacts** $I_{request}^u$ to account for electricity consumption and the **embodied impacts** $I_{request}^e$ that relates to resource extraction, hardware manufacturing and transportation. In general terms it can be expressed as follow:

$$ I_{request} = I_{request}^u  + I_{request}^e $$

$$ I_{request} = E_{request}*F_{em}+\frac{\Delta T}{\Delta L}*I_{server}^e $$

With,

* $E_{request}$ the estimated energy consumption of the server and its cooling system.
* $F_{em}$ the electricity mix that depends on the country and time.
* $\frac{\Delta T}{\Delta L}$ the hardware usage ratio i.e. the computation time over the lifetime of the hardware.
* $I_{server}^e$ the embodied impacts of the server.

Additionally, to ⚡️ **direct energy consumption** the environmental impacts are expressed in **three dimensions (multi-criteria impacts)** that are:

* 🌍 **Global Warming Potential** (GWP): Potential impact on global warming in kgCO2eq (commonly known as GHG/carbon emissions).
* 🪨 **Abiotic Depletion Potential for Elements** (ADPe): Impact on the depletion of non-living resources such as minerals or metals in kgSbeq.
* ⛽️ **Primary Energy** (PE): Total energy consumed from primary sources in MJ.
* ⛽️ **Water Consumption Footprint** (WCF): Water consumed by data centers and electricity generation power plants.

#### Principles, Data and Hypotheses

We use a **bottom-up methodology** to model impacts, meaning that we will estimate the impacts of low-level physical components to then estimate the impacts at software level (in that case an LLM inference). We also rely on **Life Cycle Approach (LCA) proxies and approach** to model both usage and embodied phases with multi-criteria impacts. If you are interested in this approach we recommend you to read the following [Boavizta](https://boavizta.org/) resources.

* [Digital & environment: How to evaluate server manufacturing footprint, beyond greenhouse gas emissions?](https://boavizta.org/en/blog/empreinte-de-la-fabrication-d-un-serveur)
* [Boavizta API automated evaluation of environmental impacts of ICT services and equipments](https://boavizta.org/en/blog/boavizta-api-automated-evaluation-of-ict-impacts-on-the-environment)
* [Boavizta API documentation](https://doc.api.boavizta.org/)

We leverage **open data to estimate the environmental impacts**, here is an exhaustive list of our data providers.

* [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) to estimate GPU energy consumption and latency based on the model architecture and number of output tokens.
* [Boavizta API](https://github.com/Boavizta/boaviztapi) to estimate server embodied impacts and base energy consumption.
* [Our World in Data](https://ourworldindata.org/), [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/) and [World Resource Institute](https://www.wri.org/) for electricity mix impacts per country.

Finally here are the **main hypotheses** we have made to compute the impacts.

* ⚠️ **We *"guesstimate"* the model architecture of proprietary LLMs when not disclosed by the provider.**
* Production setup: quantized models running on data center grade servers and GPUs such as H100.
* Electricity mixes are yearly averages.
* Ignore the following impacts: unused cloud resources, data center building, network and end-user devices... (for now)

### Equivalents

We have integrated impact equivalents to help people better understand the impacts and have reference points for standard use cases and everyday activities.

#### Request impacts

These equivalents are computed based on the request impacts only.

##### 🚶‍♂️‍➡️ Walking or 🏃‍♂️‍➡️ running distance

We compare the ⚡️ direct energy consumption with the energy consumption of someone 🚶‍♂️‍➡️ walking or 🏃‍♂️‍➡️ running. From [runningtools.com](https://www.runningtools.com/energyusage.htm) we consider the following energy values per physical activity (for someone weighing 70kg):

* 🚶‍♂️‍➡️ walking: $ 196\ kJ/km $ (speed of $ 3\ km/h $)
* 🏃‍♂️‍➡️ running: $ 294\ kJ/km $ (speed of $ 10\ km/h $)

We divide the request energy consumption by these values to compute the distance traveled.

##### 🔋 Electric Vehicle distance

We compare the ⚡️ direct energy consumption with the energy consumer by a EV car. From [selectra.info](https://selectra.info/energie/actualites/insolite/consommation-vehicules-electriques-france-2040) or [tesla.com](https://www.tesla.com/fr_fr/support/power-consumption) we consider an average value of energy consumed per kilometer of: $ 0.17\ kWh/km $.

We divide the request energy consumption by this value to compute the distance driven by an EV.

##### ⏯️ Streaming time

We compare the 🌍 GHG emissions of the request and of streaming a video. From [impactco2.fr](https://impactco2.fr/outils/comparateur?value=1&comparisons=streamingvideo), we consider that $ 1\ kgCO2eq $ is equivalent to $ 15.6\ h $ of streaming.

We multiply that value by the GHG emissions of the request to get an equivalent in hours of video streaming.

#### Scaled impacts

These equivalents are computed based on the request impacts scaled to a worldwide adoption use case. We imply that the same request is done 1% of the planet everyday for 1 year, and then compute impact equivalents.

$$
I_{scaled} = I_{request} * [1 \% \ \text{of}\ 8B\ \text{people on earth}] * 365\ \text{days}
$$

##### Number of 💨 wind turbines or ☢️ nuclear plants

We compare the ⚡️ direct energy consumption (scaled) by the energy production of wind turbines and nuclear power plants. From [ecologie.gouv.fr](https://www.ecologie.gouv.fr/eolien-terrestre) we consider that a $ 2\ MW $ wind turbine produces $ 4.2\ GWh $ a year. And from [edf.fr](https://www.edf.fr/groupe-edf/espaces-dedies/jeunes-enseignants/pour-les-jeunes/lenergie-de-a-a-z/produire-de-lelectricite/le-nucleaire-en-chiffres) we learn that a $ 900\ MW $ nuclear power plant produces $ 6\ TWh $ a year.

We divide the scaled energy consumption by these values to get the number of wind turbines or nuclear power plants needed.

##### Multiplier of 🇮🇪 Ireland electricity consumption

We compare the ⚡️ direct energy consumption (scaled) by the electricity consumption of Ireland per year. From [wikipedia.org](https://en.wikipedia.org/wiki/List_of_countries_by_electricity_consumption) we consider the Ireland electricity consumption to be $ 33\ TWh $ a year for a population of 5M.

We divide the scaled energy consumption by this value to get the equivalent number of "Ireland countries".

##### Number of ✈️ Paris ↔ New York City flights

We compare the 🌍 GHG emissions (scaled) of the request and of a return flight Paris ↔ New York City. From [impactco2.fr](https://impactco2.fr/outils/comparateur?value=1&comparisons=&equivalent=avion-pny) we consider that a return flight Paris → New York City → Paris for one passenger emits $ 1,770\ kgCO2eq $ and we consider an overall average load of 100 passengers per flight.

We divide the scaled GHG emissions by this value to get the equivalent number of return flights.

##### If you are motivated to help us test and enhance this methodology [contact us](https://codecarbon.io)! 💪
