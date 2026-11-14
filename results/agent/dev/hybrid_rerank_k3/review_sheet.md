# Review sheet — dev/hybrid_rerank_k3

Đọc từng câu: chấm `answer_grade` (0/1/2, câu có đáp án), `citation_support` (true/false cho từng citation), `abstention_correct` (câu thiếu evidence), `context_grade` (0/1/2), ghi `reason`. ID hợp lệ chưa chứng minh nguồn hỗ trợ — phải đọc đoạn trích.

## q01 — có đáp án — status: answered
**Câu hỏi:** At what level of GDP per capita relative to the United States does the median growth slowdown episode occur?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** About 11 percent of US GDP per capita — evidence: p4: “The median growth slowdown episode occurs when a country reaches about 11 percent of the gross domestic product per capita of the United States.” | p14: “The median growth slowdown episode occurs in a country-year with just 11 percent proximity to the frontier” | p3: “The median growth slowdown episode occurs when a country reaches a little more than 11 percent of the gross domestic product (GDP) per capita level of the United States.”  
**Queries:** ['median growth slowdown episode GDP per capita relative to United States']  
**Context (2549 ký tự):** ['B:wdr2024_part1:p014:c004', 'B:wdr2024_part1:p004:c000', 'B:wdr2024_part1:p013:c000']  

**Trả lời:** The median growth slowdown episode occurs when a country reaches about 11 percent of the gross domestic product per capita of the United States. This indicates that the level of GDP per capita relative to the United States at which this episode occurs is approximately 11% of U.S. GDP per capita [B:wdr2024_part1:p004:c000].

> `B:wdr2024_part1:p004:c000` (p4): Slowing Growth Key messages • Today’s 108 middle-income countries represent about 40 percent of the global economy, are home to about 75 percent of the world’s population and more than 60 percent of the world’s poor, and contribute nearly two-thirds of global carbon dioxide emissions. • Middle-income countries are prone to systematic growth slowdowns—a concept termed the “middle-income trap.” The median growth slowdown episode occurs when a country reaches about 11 percent of the gross domestic product per capita of the United States. • Although income per capita is the metric most commonly used to measure the pace of economic development, measures of average income can differ greatly, depending on the measure. • Countries with weaker institutions—and especially those with lower levels of economic and political freedom—are more susceptible to slowdowns at even lower levels of income.

## q02 — có đáp án — status: answered
**Câu hỏi:** How many middle-income economies have become high-income since 1990?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** 34 economies — evidence: p5: “Since 1990, 34 middle-income economies have transitioned to high-income status” | p7: “the 34 economies that reached high-income status between 1990 and 2021” | p2: “the 34 economies that reached high-income status between 1990 and 2021”  
**Queries:** ['middle-income economies become high-income since 1990']  
**Context (2148 ký tự):** ['B:wdr2024_part1:p005:c002', 'B:wdr2024_part1:p002:c001', 'B:wdr2024_part1:p006:c002']  

**Trả lời:** Since 1990, 34 middle-income economies have transitioned to high-income status [B:wdr2024_part1:p005:c002].

> `B:wdr2024_part1:p005:c002` (p5): Since 1990, 34 middle-income economies have transitioned to high-income status (figure 1.1).5 Thirteen benefited from deep integration with the European Union (EU)—whose economic model features vigorous trade and capital flows, freer enterprise, free worker mobility, stronger institutions, and social inclusion—at a time of relatively rapid economic growth in Western Europe. They benefited greatly from institutional and regulatory reforms that enabled transitions to a market economy, incentivized emerging economies to attract foreign direct investment and infuse new technologies into their production structures while pushing advanced economies to innovate, and fostered an environment for developing a skilled workforce. Among the other newcomers to high-income status, resource-rich economies such as Chile and Saudi Arabia benefited when they timed policy reforms to coincide with high commodity prices.

## q03 — có đáp án — status: answered
**Câu hỏi:** By which year does Viet Nam plan to reach high-income status?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** 2045 — evidence: p6: “with a transition to high-income status by 2045”  
**Queries:** ['Viet Nam high-income status year']  
**Context (2521 ký tự):** ['B:wdr2024_part1:p006:c000', 'B:wdr2024_part1:p006:c002', 'B:wdr2024_part1:p005:c002']  

**Trả lời:** Viet Nam plans to transition to high-income status by 2045, as outlined in its Socio-Economic Development Strategy 2021–2030, which aims to sustain GDP per capita growth of 7 percent through this decade. [B:wdr2024_part1:p006:c000]

> `B:wdr2024_part1:p006:c000` (p6): the nation into a developed economy by 2047— the hundredth year of independence. In Viet Nam, its Socio-Economic Development Strategy 2021–2030 outlines a plan to sustain GDP per capita growth of 7 percent through this decade, with a transition to high-income status by 2045. In South Africa, the 2030 National Development Plan has prioritized raising its income per capita from US$2,800 in 2010 to US$7 ,000 by 2030. Other middle-income countries have similar aspirations. But the growth prospects of middle-income countries are not improving. Over the last decade, the global economy has gone from healthy to hobbling and from largely integrated to increasingly fragmented.7 Foreign trade and investment channels are also becoming more constricted—or at least encumbered—by geopolitical tensions.

## q04 — có đáp án — status: answered
**Câu hỏi:** What income cutoff did the very first World Development Report use to separate poor countries from middle-income ones?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** US$250 GNI per capita — evidence: p8: “using a threshold of US$250 gross national income (GNI) per capita between the groups” | p4: “Middle-income countries were defined as those with annual income per capita of over US$250.”  
**Queries:** ['first World Development Report income cutoff poor countries middle-income']  
**Context (2664 ký tự):** ['B:wdr2024_part1:p004:c001', 'B:wdr2024_part1:p007:c004', 'B:wdr2024_part1:p008:c002']  

**Trả lời:** The very first World Development Report, published in 1978, used an income cutoff of US$250 per capita to separate low-income countries from middle-income ones. Countries with a gross national income (GNI) per capita of US$250 or less were classified as low-income, while those with more than US$250 were classified as middle-income [B:wdr2024_part1:p007:c004].

> `B:wdr2024_part1:p007:c004` (p7): Country definitions are based on the first World Development Report (World Bank 1978), in which low-income countries have gross national income (GNI) per capita of US$250 or less, and middle-income countries have GNI per capita of more than US$250; industrialized (high-income) countries consist of member countries of the Organisation for Economic Co-operation and Development (OECD), except for Greece, Portugal, Spain, and Türkiye, which are classified as middle-income countries. Share of US GNI per capita (%) Middle-income countries Middle-income countries, excluding China

## q05 — có đáp án — status: answered
**Câu hỏi:** At what value was the high-income threshold originally set in the 1989 Board paper?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** GNI per capita of US$6,000 in 1987 prices — evidence: p9: “was set at GNI per capita of US$6,000 in 1987 prices”  
**Queries:** ['high-income threshold 1989 Board paper']  
**Context (2472 ký tự):** ['B:wdr2024_part1:p009:c001', 'B:wdr2024_part1:p009:c000', 'B:wdr2024_part1:p008:c003']  

**Trả lời:** The high-income threshold was originally set at GNI per capita of US$6,000 in 1987 prices in a paper presented to the World Bank’s Board of Executive Directors in January 1989. This level has been updated over time for international inflation. [B:wdr2024_part1:p009:c001]

> `B:wdr2024_part1:p009:c001` (p9): The high-income threshold does not relate to a cutoff derived from the operational guidelines, but was set at GNI per capita of US$6,000 in 1987 prices in a paper presented to the World Bank’s Board of Executive Directors in January 1989, which also reconfirmed the low- and lower- middle- income threshold levels.f The US$6,000 level has been updated over time for what is called “international inflation,” defined as the average inflation rates of Japan, the United Kingdom, the United States, and the euro area. The choice of the high-income threshold was made to address anomalies in the classification of high-income and industrialized economies used in the World Bank’s World Development Indicators prior to that point. Under this current classification method, Zambia (with income per capita of US$1,170) and Bulgaria (with income per capita of US$13,250) are both middle-income economies.

## q06 — có đáp án — status: answered
**Câu hỏi:** How does Turkiye's GDP per capita relative to the United States differ when adjusted for PPP versus using market exchange rates?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** Nearly 50 percent with PPP, less than 15 percent at market exchange rates — evidence: p10: “is nearly 50 percent when adjusted for PPP but less than 15 percent using market exchange rates”  
**Queries:** ['Turkiye GDP per capita PPP market exchange rates comparison United States']  
**Context (3109 ký tự):** ['B:wdr2024_part1:p010:c000', 'B:wdr2024_part1:p008:c002', 'B:wdr2024_part1:p015:c000']  

**Trả lời:** Türkiye’s GDP per capita relative to the United States is nearly 50 percent when adjusted for purchasing power parity (PPP) but less than 15 percent using market exchange rates [B:wdr2024_part1:p010:c000].

> `B:wdr2024_part1:p010:c000` (p10): high-income country. Yet when adjusted for purchasing power, Türkiye’s GDP per capita is higher than Chile’s. The country for which both measures are defined as identical is the United States because purchasing power in any country is measured relative to what a dollar can buy in the United States. Türkiye’s GDP per capita relative to that of the United States is nearly 50 percent when adjusted for PPP but less than 15 percent using market exchange rates. For Chile, the numbers are, respectively, 40 percent and 20 percent. PPP adjustments have been criticized for their inability to reflect the complexity and diversity of economic production and capabilities in indi-vidual economies.12 The adjustments do not consider quality or productivity differences among countries in the production of tradable as well as nontradable goods and services, including infrastructure, health care, and education. However, recent assessments of PPPs appear to be highly correlated with economic activity.

## q07 — có đáp án — status: answered
**Câu hỏi:** How much did Korea's R&D spending rise as a share of GDP between 1980 and 1990?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** From 0.5 percent of GDP in 1980 to 1.6 percent in 1990 — evidence: p12: “spending on R&D jumped from 0.5 percent of GDP in 1980 to 1.6 percent in 1990”  
**Queries:** ['Korea R&D spending share of GDP 1980 1990']  
**Context (3094 ký tự):** ['B:wdr2024_part1:p012:c002', 'B:wdr2024_part1:p012:c001', 'B:wdr2024_part1:p025:c002']  

**Trả lời:** Korea's R&D spending rose from 0.5 percent of GDP in 1980 to 1.6 percent in 1990, indicating an increase of 1.1 percentage points over that decade. [B:wdr2024_part1:p012:c002]

> `B:wdr2024_part1:p012:c002` (p12): Korea’s spending on R&D jumped from 0.5 percent of GDP in 1980 to 1.6 percent in 1990 when Korea was still an upper-middle-income country. Private R&D expenditures increased by an unprecedented 26 times from 1980 to 1990 and exceeded 80 percent of total R&D spending by the end of the 1990s. In parallel, Korea invested heavily in human capital and ensured that job creation was matched with the needed supply of skills at the different stages of development— vocational and technical secondary, STEM (science, technology, engineering, and mathematics) education, and R&D accelerators—which was carried out more effectively than by much richer countries. Third, Korea got better at regulating the relationships among large, medium, and small firms. Initially, large firms were favored as the instrument for infusing new technologies into the economy.

## q08 — có đáp án — status: answered
**Câu hỏi:** How do Eichengreen, Park, and Shin define a growth slowdown?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** A decline in the seven-year average GDP per capita growth rate by at least 2 percentage points, with prior growth above 3.5 percent — evidence: p13: “They define a slowdown as a decline in the seven-year average growth rate of gross domestic product (GDP) per capita by at least 2 percentage points”  
**Queries:** ['Eichengreen Park Shin growth slowdown definition']  
**Context (3153 ký tự):** ['B:wdr2024_part1:p013:c000', 'B:wdr2024_part1:p013:c001', 'B:wdr2024_part1:p014:c000']  

**Trả lời:** Eichengreen, Park, and Shin define a growth slowdown as a decline in the seven-year average growth rate of gross domestic product (GDP) per capita by at least 2 percentage points, with growth being higher than 3.5 percent in the preceding years. They also limit slowdowns to cases where GDP per capita is greater than US$10,000 in 2005 constant international prices adjusted for purchasing power parity (PPP) and find that slowdowns occur when GDP per capita reaches about US$16,540 (in 2005 constant international PPP prices) [B:wdr2024_part1:p013:c000].

> `B:wdr2024_part1:p013:c000` (p13): Box 1.3 Identifying growth slowdowns Several studies have examined the reasons for growth slowdowns. Eichengreen, Park, and Shin (2011) identify frequent slowdowns in middle-income countries. They define a slowdown as a decline in the seven-year average growth rate of gross domestic product (GDP) per capita by at least 2 percentage points, with growth being higher than 3.5 percent in the preceding years. In addition, they limit slowdowns to cases in which GDP per capita is greater than US$10,000 in 2005 constant international prices adjusted for purchasing power parity (PPP). They discover slowdowns when GDP per capita reaches about US$16,540 (in 2005 constant international PPP prices). Extensions of the analysis indicate that growth in middle-income countries slows even at points early in the middle-income stage: specifically, in the range of US$10,000–US$11,000 GDP per capita (in 2005 constant prices) and in the range of US$15,000–US$16,000 (in 2005 constant prices).

## q09 — có đáp án — status: answered
**Câu hỏi:** Compared with rich countries, how much more prone are middle-income countries to growth slowdowns?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** Three times as likely — evidence: p14: “is three times as likely to experience a growth slowdown compared with a high-income country”  
**Queries:** ['middle-income countries growth slowdowns compared with rich countries']  
**Context (2589 ký tự):** ['B:wdr2024_part1:p014:c001', 'B:wdr2024_part1:p004:c000', 'B:wdr2024_part1:p014:c002']  

**Trả lời:** Middle-income countries are three times as likely to experience a growth slowdown compared with high-income countries [B:wdr2024_part1:p014:c001].

> `B:wdr2024_part1:p014:c001` (p14): The median growth slowdown episode occurs in a country-year with just 11 percent proximity to the frontier, and the mean episode occurs at 21 percent proximity to the frontier—approximately the 75th percentile in the distribution. Together, these median and mean measures imply that a majority of growth slowdowns take place in middle-income countries (figure 1.4). In fact, a middle-income country is three times as likely to experience a growth slowdown compared with a high-income country. Using the World Bank’s Long Term Growth Model (LTGM),18 figure 1.5 sheds more light on growth slowdowns in low- and middle-income countries.

## q10 — có đáp án — status: answered
**Câu hỏi:** In the Spotlight section, how much of productivity growth in developing countries comes from efficient allocation of factors of production?  
**Filter người dùng:** {'section': 'spotlight'}  
**Đáp án chuẩn (chỉ để chấm):** About 25 percent — evidence: p17: “efficient allocation of the factors of production accounts for about 25 percent of productivity growth in developing countries”  
**Queries:** ['Spotlight section productivity growth developing countries efficient allocation of factors of production']  
**Context (2788 ký tự):** ['B:wdr2024_part1:p017:c002', 'B:wdr2024_part1:p017:c000', 'B:wdr2024_part1:p018:c001']  

**Trả lời:** Efficient allocation of the factors of production accounts for about 25 percent of productivity growth in developing countries. This efficiency boosts job and output growth and creates positive spillovers for other businesses along the value chain. Additionally, reducing productivity-constraining distortions encourages productive firms to infuse new technologies and grow [B:wdr2024_part1:p017:c002].

> `B:wdr2024_part1:p017:c002` (p17): At this stage of growth, countries also need to improve the allocation of resources to their most productive firms. In fact, efficient allocation of the factors of production accounts for about 25 percent of productivity growth in developing countries.4 Efficiency in allocating resources boosts job and output growth as well as creates positive spillovers for other businesses along the value chain.5 By reducing productivity-constraining distortions—defined as policy measures that curb the expansion and growth of productive firms— countries can encourage productive firms to infuse new technologies and grow. Finally, when countries focus on innovation, there is a rise in the number of their patents and the importance of these patents in the global production of knowledge. Talent Countries need a more skilled workforce as their production processes become more complex with

## q11 — có đáp án — status: answered
**Câu hỏi:** By 2008, how productive was the average Brazilian manufacturing worker compared with an American worker?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** 17 percent — evidence: p21: “By 2008, this ratio had fallen to 17 percent.”  
**Queries:** ['Brazilian manufacturing worker productivity compared to American worker 2008']  
**Context (2563 ký tự):** ['B:wdr2024_part1:p021:c002', 'B:wdr2024_part1:p021:c003', 'B:wdr2024_part1:p019:c002']  

**Trả lời:** By 2008, the average Brazilian manufacturing worker was 17 percent as productive as his American counterpart [B:wdr2024_part1:p021:c002].

> `B:wdr2024_part1:p021:c002` (p21): Introduction In Brazil in the early 1970s, after several decades of impressive output growth, the average worker in the manufacturing sector was more than 40 percen t as productive as his American coun terpart. By 2008, this ratio had fallen to 17 percent. Up until about 1980, Brazil implemented protectionist policies from foreign competition and provided incentives to substitute imports by domestic manufacturers. Although all these policies were intended to make Brazil more competitive, they led to a decline in the productivity of Brazilian workers, and enterprises became less competitive than those in the United States.1 Meanwhile, in Northeast Asia something completely different was happening in the Republic of Korea and Taiwan, China. In the 1970s, the productivity of Korea’s manufacturing workers was less than one-tenth of their American counterparts.

## q12 — có đáp án — status: answered
**Câu hỏi:** If capital endowments were the only difference between middle-income and high-income countries, what would a typical middle-income country's GNI be relative to the United States?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** About 75 percent of the United States — evidence: p23: “would be about 75 percent that of the United States”  
**Queries:** ['middle-income countries GNI relative to United States capital endowments']  
**Context (2569 ký tự):** ['B:wdr2024_part1:p023:c001', 'B:wdr2024_part1:p023:c000', 'B:wdr2024_part1:p007:c003']  

**Trả lời:** If capital endowments were the only economically relevant difference between middle-income and high-income countries, the gross national income (GNI) of a typical middle-income country would be about 75 percent that of the United States. [B:wdr2024_part1:p023:c000]

> `B:wdr2024_part1:p023:c000` (p23): Economic development = structural change As described in chapter 1, the term “middle- income trap” refers to the risk of an economic slowdown or stagnation if a country fails to adapt its policies and institutions to changing economic and structural needs.3 Strategies based on factor accumulation alone are likely to steadily worsen results—a natural occurrence as the marginal productivity of capital declines. Even if all middle -income countries enjoyed the enabling conditions of peace, freedom, factor mobility, and rule of law, the returns from capital investment alone would decline too sharply to support the countries’ sustained and ongoing economic growth.4 If capital endowments were the only economi-cally relevant difference between middle- income and high-income countries today, the gross national income (GNI) of a typical middle-income country would be about 75 percent that of the United States.

## q13 — có đáp án — status: answered
**Câu hỏi:** What fraction of the world's science and engineering graduates now come from middle-income countries?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** Three-quarters — evidence: p26: “three-quarters of STEM graduates are now in middle-income countries”  
**Queries:** ["fraction of the world's science and engineering graduates from middle-income countries"]  
**Context (2461 ký tự):** ['B:wdr2024_part1:p027:c003', 'B:wdr2024_part1:p026:c000', 'B:wdr2024_part1:p026:c001']  

**Trả lời:** Three-quarters of STEM graduates are now in middle-income countries [B:wdr2024_part1:p026:c001].

> `B:wdr2024_part1:p026:c001` (p26): Encouragingly, three-quarters of STEM graduates are now in middle-income countries, and Chinese and Indian STEM graduates make up about half of global STEM graduates (figure 2.4). The example of Korea, the only country ever to sustain economic growth that averaged more than 5 percent for more than 50 years, is especially illustrative. How did Korean industry do it? Domestic firms such as Samsung embarked on a journey that began with infusion. By licensing technologies from Sanyo and NEC in Japan, Samsung transitioned from making noodles Source: WDR 2024 team using DataBank: Jobs, World Bank, Washington, DC, https://databank.worldbank.org/source / jobs; WDI (World Development Indicators) (Data Catalog), World Bank, Washington, DC, https://datacatalog.worldbank.org / search/dataset/0037712 .

## q14 — có đáp án — status: answered
**Câu hỏi:** According to the Structural Stasis chapter, how did Korea subsidize the adoption of foreign technologies and innovation?  
**Filter người dùng:** {'section': 'ch2_structural_stasis'}  
**Đáp án chuẩn (chỉ để chấm):** Through tax credits for royalty payments or R&D expenditures — evidence: p25: “Korea subsidized the adoption of foreign technologies and innovation through tax credits”  
**Queries:** ['Korea subsidize adoption of foreign technologies innovation Structural Stasis chapter']  
**Context (2958 ký tự):** ['B:wdr2024_part1:p025:c002', 'B:wdr2024_part1:p025:c001', 'B:wdr2024_part1:p028:c003']  

**Trả lời:** Korea subsidized the adoption of foreign technologies and innovation through tax credits for royalty payments or research and development (R&D) expenditures. Initially, this policy focused on technology adoption when the technology gap with foreign firms was significant. As Korean conglomerates began to catch up, the approach shifted towards supporting innovation. Additionally, public support for these initiatives was monitored and evaluated, with data on innovation grants made publicly available. Firms could receive a reimbursement equivalent to a percentage of their expenditures on adoption fees or R&D, indicating a structured subsidy system for technological investment in Korea. [B:wdr2024_part1:p025:c002][B:wdr2024_part1:p025:c001][B:wdr2024_part1:p028:c003]

> `B:wdr2024_part1:p025:c002` (p25): Specifically, firms received tax credits for royalty payments or research and development (R&D) expenditures. The policy first subsidized technology adoption when the technology gap with foreign firms was large. But as Korean conglomerates caught up with foreign firms, the approach gradually shifted toward supporting innovation. Korean policy makers ensured that public support was monitored and evaluated, and data on innovation grants were made publicly available. • Malaysia. Malaysia became a successful industrialized country through infusion-centered and export-oriented growth that replaced import substitution policies in the mid-1980s. Technology embodied in foreign direct investment (FDI) was important for developing and structuring the country’s industrial base. Malaysia offered a spectrum of tax incentives to attract FDI through the Promotion of Investment Act in 1986.9 Malaysia’s growth in the 1980s was marked by large productivity gains from adopting and diffusing technology.

> `B:wdr2024_part1:p025:c001` (p25): • Postwar Europe. The onset of the European Golden Age was powered by infusion. The two world wars in the first half of the twen-tieth century destroyed much of Europe’s capital stock and skills. And the exodus of talent in the interwar years meant that Europe lagged behind the United States in technology. 7 The Marshall Plan was developed to transfer technologies from the United States to Europe. European managers were sent to the United States to acquire skills, and businesses could obtain loans to purchase technologically advanced American capital goods under the US Productivity Program. As a result, Europe rapidly adopted modern technologies and best practices, allowing Western European countries to accomplish in 30 years what might otherwise have taken twice as long.8 • Korea. An important component of industrial policy in Korea was incentives for technological investment. In particular, Korea subsidized the adoption of foreign technologies and innovation through tax credits.

> `B:wdr2024_part1:p028:c003` (p28): The time, manner and drawing, specification and other technical document as well (a) CO., LTD. AND Sources: Panel a: National Archives of Korea, https://www.archives.go.kr/english/index.jsp . Panel b: Choi and Shim 2024. Note: Panel b shows the adoption subsidy rate alongside the innovation (R&D) subsidy rate, calculated using the tax credit rate and the corporate tax rate. For example, a 30 percent subsidy rate indicates that firms can receive a reimbursement equivalent to 30 percent of their expenditures on adoption fees or R&D. R&D = research and development. Figure 2.5 Calibrating policies to a country’s stage of development: From imitation to innovation in the Republic of Korea

## q15 — có đáp án — status: answered
**Câu hỏi:** How long is it estimated to take today's middle-income countries to move from an aging society to an aged society?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** About 26 years — evidence: p36: “transitioning from an aging society to an aged society is estimated to take about 26 years for today’s middle-income countries”  
**Queries:** ['middle-income countries aging society aged society transition duration']  
**Context (2659 ký tự):** ['B:wdr2024_part1:p036:c000', 'B:wdr2024_part1:p036:c001', 'B:wdr2024_part1:p035:c003']  

**Trả lời:** It is estimated to take about 26 years for today's middle-income countries to transition from an aging society to an aged society. This is significantly faster than the historical transitions observed in high-income countries, which took about 61 years on average. [B:wdr2024_part1:p036:c000]

> `B:wdr2024_part1:p036:c000` (p36): Box 3.1 Graying growth Historically, demographic dividends have fostered economic growth in many countries. An increase in the working-age population and a consequent decrease in dependency ratios free up resources to be spent on education, health care, employment, and social protection schemes.a However, the world is aging rapidly and fertility rates are declining rapidly,b which will especially affect middle-income countries projected to face labor crunches in the coming decades. In fact, today’s middle-income countries are aging more rapidly than high-income countries did in the past. Transitioning from an aging society to an aged society took about 61 years in today’s high-income countries and as long as 69 years in the United States and 115 years in France.c By contrast, transitioning from an aging society to an aged society is estimated to take about 26 years for today’s middle-income countries (figure B3.1.1).

## q16 — có đáp án — status: answered
**Câu hỏi:** How has the yearly count of new harmful trade measures changed over the past ten years?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** It doubled — evidence: p38: “the number of new harmful trade measures enacted per year doubled over the last decade”  
**Queries:** ['yearly count of new harmful trade measures past ten years']  
**Context (2239 ký tự):** ['B:wdr2024_part1:p038:c002', 'B:wdr2024_part1:p039:c003', 'B:wdr2024_part1:p039:c002']  

**Trả lời:** The number of new harmful trade measures enacted per year has doubled over the last decade. This indicates a significant increase in such measures during this period [B:wdr2024_part1:p038:c002].

> `B:wdr2024_part1:p038:c002` (p38): increasing: the number of new harmful trade measures enacted per year doubled over the last decade (figure 3.1). Source: WDR 2024 team using the GTA (Global Trade Alert) database, St. Gallen Endowment for Prosperity through Trade, University of St. Gallen, St. Gallen, Switzerland, https://www.globaltradealert.org/data_extraction . Note: Measuring trade policies is fraught with challenges, and the GTA database may overrepresent countries that issue a relatively high quantity of legislative documents or those with greater regulatory transparency. The plotted lines indicate global trade policies that were introduced in the corresponding year. Helpful trade policies include interventions that liberalize on a nondiscriminatory basis or improve the transparency of a relevant policy. Harmful trade policies include interventions that discriminate against foreign commercial interests.

## u01 — THIẾU evidence — status: abstain
**Câu hỏi:** By which year does Thailand aim to reach high-income status?  
**Filter người dùng:** None  
**Lý do thiếu evidence:** Thailand không xuất hiện ở bất kỳ trang nào (grep 'Thailand' trên 157 chunk và toàn văn pdftotext = 0). Câu gần chủ đề với q03 (Viet Nam 2045) và mục tiêu của India 2047 ở p6.  
**Queries:** ['Thailand high-income status target year', 'Thailand high-income status target year 2047', 'Thailand high-income status 2047']  
**Context (4103 ký tự):** ['B:wdr2024_part1:p002:c001', 'B:wdr2024_part1:p006:c002', 'B:wdr2024_part1:p006:c000', 'B:wdr2024_part1:p006:c001', 'B:wdr2024_part1:p005:c002']  

**Trả lời:** The documents do not contain enough evidence.

## u02 — THIẾU evidence — status: abstain
**Câu hỏi:** What was Bulgaria's R&D expenditure as a share of GDP in 2021?  
**Filter người dùng:** None  
**Lý do thiếu evidence:** Box 2.2 (p30) chỉ nêu R&D intensity của Estonia (1,75%) và Poland (1,3%) năm 2021; với Bulgaria chỉ có tăng năng suất 1,4%/năm (bẫy gần nghĩa). grep 'Bulgaria' toàn văn: không có số R&D cho Bulgaria.  
**Queries:** ['Bulgaria R&D expenditure share of GDP 2021']  
**Context (3022 ký tự):** ['B:wdr2024_part1:p030:c001', 'B:wdr2024_part1:p031:c003', 'B:wdr2024_part1:p012:c002']  

**Trả lời:** The documents do not contain enough evidence.

