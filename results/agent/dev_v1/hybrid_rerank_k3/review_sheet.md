# Review sheet — dev/hybrid_rerank_k3

Đọc từng câu: chấm `answer_grade` (0/1/2, câu có đáp án), `citation_support` (true/false cho từng citation), `abstention_correct` (câu thiếu evidence), `context_grade` (0/1/2), ghi `reason`. ID hợp lệ chưa chứng minh nguồn hỗ trợ — phải đọc đoạn trích.

## q01 — có đáp án — status: answered
**Câu hỏi:** At what level of GDP per capita relative to the United States does the median growth slowdown episode occur?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** About 11 percent of US GDP per capita — evidence: p4: “The median growth slowdown episode occurs when a country reaches about 11 percent of the gross domestic product per capita of the United States.” | p14: “The median growth slowdown episode occurs in a country-year with just 11 percent proximity to the frontier” | p3: “The median growth slowdown episode occurs when a country reaches a little more than 11 percent of the gross domestic product (GDP) per capita level of the United States.”  
**Queries:** ['median growth slowdown episode GDP per capita relative to United States']  
**Context (2549 ký tự):** ['B:wdr2024_part1:p014:c004', 'B:wdr2024_part1:p004:c000', 'B:wdr2024_part1:p013:c000']  

**Trả lời:** The median growth slowdown episode occurs when a country reaches about 11 percent of the GDP per capita of the United States [B:wdr2024_part1:p004:c000].

> `B:wdr2024_part1:p004:c000` (p4): Slowing Growth Key messages • Today’s 108 middle-income countries represent about 40 percent of the global economy, are home to about 75 percent of the world’s population and more than 60 percent of the world’s poor, and contribute nearly two-thirds of global carbon dioxide emissions. • Middle-income countries are prone to systematic growth slowdowns—a concept termed the “middle-income trap.” The median growth slowdown episode occurs when a country reaches about 11 percent of the gross domestic product per capita of the United States. • Although income per capita is the metric most commonly used to measure the pace of economic development, measures of average income can differ greatly, depending on the measure. • Countries with weaker institutions—and especially those with lower levels of economic and political freedom—are more susceptible to slowdowns at even lower levels of income.

## q02 — có đáp án — status: abstain
**Câu hỏi:** How many middle-income economies have become high-income since 1990?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** 34 economies — evidence: p5: “Since 1990, 34 middle-income economies have transitioned to high-income status” | p7: “the 34 economies that reached high-income status between 1990 and 2021” | p2: “the 34 economies that reached high-income status between 1990 and 2021”  
**Queries:** ['middle-income economies become high-income since 1990']  
**Context (2148 ký tự):** ['B:wdr2024_part1:p005:c002', 'B:wdr2024_part1:p002:c001', 'B:wdr2024_part1:p006:c002']  

**Trả lời:** Không đủ bằng chứng trong tài liệu để trả lời.

## q03 — có đáp án — status: abstain
**Câu hỏi:** By which year does Viet Nam plan to reach high-income status?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** 2045 — evidence: p6: “with a transition to high-income status by 2045”  
**Queries:** ['Viet Nam high-income status year']  
**Context (2521 ký tự):** ['B:wdr2024_part1:p006:c000', 'B:wdr2024_part1:p006:c002', 'B:wdr2024_part1:p005:c002']  

**Trả lời:** Không đủ bằng chứng trong tài liệu để trả lời.

## q04 — có đáp án — status: answered
**Câu hỏi:** What income cutoff did the very first World Development Report use to separate poor countries from middle-income ones?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** US$250 GNI per capita — evidence: p8: “using a threshold of US$250 gross national income (GNI) per capita between the groups” | p4: “Middle-income countries were defined as those with annual income per capita of over US$250.”  
**Queries:** ['first World Development Report income cutoff poor countries middle-income']  
**Context (2664 ký tự):** ['B:wdr2024_part1:p004:c001', 'B:wdr2024_part1:p007:c004', 'B:wdr2024_part1:p008:c002']  

**Trả lời:** The very first World Development Report, published in 1978, used an income cutoff of US$250 per capita to separate low-income countries from middle-income countries. Low-income countries were defined as those with gross national income (GNI) per capita of US$250 or less, while middle-income countries had GNI per capita of more than US$250 [B:wdr2024_part1:p004:c001][B:wdr2024_part1:p007:c004][B:wdr2024_part1:p008:c002].

> `B:wdr2024_part1:p004:c001` (p4): Introduction The problem of economic growth in middle- inco me economies has been a concern of development policy practitioners for at least five decades. In the first World Development Report, published in 1978, “middle-income” was an omnibus term applied to countries with diverse economic characteristics at various stages of development.1 Middle-income countries were defined as those with annual income per capita of over US$250.2 By that definition, 58 countries, home to about 900 million people, were designated middle-income. Despite the diversity, World Development Report 1978 identified two characteristics that distinguished middle-income from low- incom e countries: • Their growth prospects were more sen-sitive to economic conditions in the industrialized (high-income) countries, particularly the environment for trade and commercial capital flows. • They had more resources available to raise the living standards of the poor.

> `B:wdr2024_part1:p007:c004` (p7): Country definitions are based on the first World Development Report (World Bank 1978), in which low-income countries have gross national income (GNI) per capita of US$250 or less, and middle-income countries have GNI per capita of more than US$250; industrialized (high-income) countries consist of member countries of the Organisation for Economic Co-operation and Development (OECD), except for Greece, Portugal, Spain, and Türkiye, which are classified as middle-income countries. Share of US GNI per capita (%) Middle-income countries Middle-income countries, excluding China

> `B:wdr2024_part1:p008:c002` (p8): According to World Bank estimates that use market exchange rates, Türkiye is a middle- income c ountry, and Chile is a Box 1.1 Misunderstanding through misclassification The World Bank’s income classification method for grouping countries was first presented in the 1978 World Development Report .a It introduced groupings of “low-income” and “middle-income” countries using a threshold of US$250 gross national income (GNI) per capita between the groups. The low-income threshold was set in keeping with the guidelines for procurement of goods and services for civil works projects for countries eligible for assistance from the International Development Association (IDA), the organization in the World Bank Group that supports the world’s least developed countries. Specifically, the threshold was based on the “civil works preference” operational guideline for IDA countries.

## q05 — có đáp án — status: abstain
**Câu hỏi:** At what value was the high-income threshold originally set in the 1989 Board paper?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** GNI per capita of US$6,000 in 1987 prices — evidence: p9: “was set at GNI per capita of US$6,000 in 1987 prices”  
**Queries:** ['high-income threshold 1989 Board paper']  
**Context (2472 ký tự):** ['B:wdr2024_part1:p009:c001', 'B:wdr2024_part1:p009:c000', 'B:wdr2024_part1:p008:c003']  

**Trả lời:** Không đủ bằng chứng trong tài liệu để trả lời.

## q06 — có đáp án — status: answered
**Câu hỏi:** How does Turkiye's GDP per capita relative to the United States differ when adjusted for PPP versus using market exchange rates?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** Nearly 50 percent with PPP, less than 15 percent at market exchange rates — evidence: p10: “is nearly 50 percent when adjusted for PPP but less than 15 percent using market exchange rates”  
**Queries:** ['Turkiye GDP per capita United States PPP market exchange rates']  
**Context (3109 ký tự):** ['B:wdr2024_part1:p010:c000', 'B:wdr2024_part1:p008:c002', 'B:wdr2024_part1:p015:c000']  

**Trả lời:** Türkiye’s GDP per capita relative to the United States is nearly 50 percent when adjusted for purchasing power parity (PPP) but less than 15 percent using market exchange rates [B:wdr2024_part1:p010:c000].

> `B:wdr2024_part1:p010:c000` (p10): high-income country. Yet when adjusted for purchasing power, Türkiye’s GDP per capita is higher than Chile’s. The country for which both measures are defined as identical is the United States because purchasing power in any country is measured relative to what a dollar can buy in the United States. Türkiye’s GDP per capita relative to that of the United States is nearly 50 percent when adjusted for PPP but less than 15 percent using market exchange rates. For Chile, the numbers are, respectively, 40 percent and 20 percent. PPP adjustments have been criticized for their inability to reflect the complexity and diversity of economic production and capabilities in indi-vidual economies.12 The adjustments do not consider quality or productivity differences among countries in the production of tradable as well as nontradable goods and services, including infrastructure, health care, and education. However, recent assessments of PPPs appear to be highly correlated with economic activity.

## q07 — có đáp án — status: abstain
**Câu hỏi:** How much did Korea's R&D spending rise as a share of GDP between 1980 and 1990?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** From 0.5 percent of GDP in 1980 to 1.6 percent in 1990 — evidence: p12: “spending on R&D jumped from 0.5 percent of GDP in 1980 to 1.6 percent in 1990”  
**Queries:** ['Korea R&D spending share of GDP 1980 1990']  
**Context (3094 ký tự):** ['B:wdr2024_part1:p012:c002', 'B:wdr2024_part1:p012:c001', 'B:wdr2024_part1:p025:c002']  

**Trả lời:** Không đủ bằng chứng trong tài liệu để trả lời.

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

## q10 — có đáp án — status: abstain
**Câu hỏi:** In the Spotlight section, how much of productivity growth in developing countries comes from efficient allocation of factors of production?  
**Filter người dùng:** {'section': 'spotlight'}  
**Đáp án chuẩn (chỉ để chấm):** About 25 percent — evidence: p17: “efficient allocation of the factors of production accounts for about 25 percent of productivity growth in developing countries”  
**Queries:** ['Spotlight section productivity growth developing countries efficient allocation of factors of production']  
**Context (2788 ký tự):** ['B:wdr2024_part1:p017:c002', 'B:wdr2024_part1:p017:c000', 'B:wdr2024_part1:p018:c001']  

**Trả lời:** Không đủ bằng chứng trong tài liệu để trả lời.

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
**Queries:** ['capital endowments middle-income high-income countries GNI relative to United States']  
**Context (2569 ký tự):** ['B:wdr2024_part1:p023:c001', 'B:wdr2024_part1:p023:c000', 'B:wdr2024_part1:p007:c003']  

**Trả lời:** If capital endowments were the only economically relevant difference between middle-income and high-income countries, the gross national income (GNI) of a typical middle-income country would be about 75 percent that of the United States [B:wdr2024_part1:p023:c000].

> `B:wdr2024_part1:p023:c000` (p23): Economic development = structural change As described in chapter 1, the term “middle- income trap” refers to the risk of an economic slowdown or stagnation if a country fails to adapt its policies and institutions to changing economic and structural needs.3 Strategies based on factor accumulation alone are likely to steadily worsen results—a natural occurrence as the marginal productivity of capital declines. Even if all middle -income countries enjoyed the enabling conditions of peace, freedom, factor mobility, and rule of law, the returns from capital investment alone would decline too sharply to support the countries’ sustained and ongoing economic growth.4 If capital endowments were the only economi-cally relevant difference between middle- income and high-income countries today, the gross national income (GNI) of a typical middle-income country would be about 75 percent that of the United States.

## q13 — có đáp án — status: answered
**Câu hỏi:** What fraction of the world's science and engineering graduates now come from middle-income countries?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** Three-quarters — evidence: p26: “three-quarters of STEM graduates are now in middle-income countries”  
**Queries:** ["fraction of world's science and engineering graduates from middle-income countries"]  
**Context (2461 ký tự):** ['B:wdr2024_part1:p027:c003', 'B:wdr2024_part1:p026:c000', 'B:wdr2024_part1:p026:c001']  

**Trả lời:** Three-quarters of STEM graduates are now in middle-income countries, with Chinese and Indian STEM graduates making up about half of global STEM graduates [B:wdr2024_part1:p026:c001].

> `B:wdr2024_part1:p026:c001` (p26): Encouragingly, three-quarters of STEM graduates are now in middle-income countries, and Chinese and Indian STEM graduates make up about half of global STEM graduates (figure 2.4). The example of Korea, the only country ever to sustain economic growth that averaged more than 5 percent for more than 50 years, is especially illustrative. How did Korean industry do it? Domestic firms such as Samsung embarked on a journey that began with infusion. By licensing technologies from Sanyo and NEC in Japan, Samsung transitioned from making noodles Source: WDR 2024 team using DataBank: Jobs, World Bank, Washington, DC, https://databank.worldbank.org/source / jobs; WDI (World Development Indicators) (Data Catalog), World Bank, Washington, DC, https://datacatalog.worldbank.org / search/dataset/0037712 .

## q14 — có đáp án — status: abstain
**Câu hỏi:** According to the Structural Stasis chapter, how did Korea subsidize the adoption of foreign technologies and innovation?  
**Filter người dùng:** {'section': 'ch2_structural_stasis'}  
**Đáp án chuẩn (chỉ để chấm):** Through tax credits for royalty payments or R&D expenditures — evidence: p25: “Korea subsidized the adoption of foreign technologies and innovation through tax credits”  
**Queries:** ['Korea subsidize adoption of foreign technologies and innovation Structural Stasis chapter']  
**Context (2958 ký tự):** ['B:wdr2024_part1:p025:c002', 'B:wdr2024_part1:p025:c001', 'B:wdr2024_part1:p028:c003']  

**Trả lời:** Không đủ bằng chứng trong tài liệu để trả lời.

## q15 — có đáp án — status: abstain
**Câu hỏi:** How long is it estimated to take today's middle-income countries to move from an aging society to an aged society?  
**Filter người dùng:** None  
**Đáp án chuẩn (chỉ để chấm):** About 26 years — evidence: p36: “transitioning from an aging society to an aged society is estimated to take about 26 years for today’s middle-income countries”  
**Queries:** ['middle-income countries aging society aged society transition duration']  
**Context (2659 ký tự):** ['B:wdr2024_part1:p036:c000', 'B:wdr2024_part1:p036:c001', 'B:wdr2024_part1:p035:c003']  

**Trả lời:** Không đủ bằng chứng trong tài liệu để trả lời.

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

**Trả lời:** The documents do not contain enough evidence regarding the specific year Thailand aims to reach high-income status.

## u02 — THIẾU evidence — status: abstain
**Câu hỏi:** What was Bulgaria's R&D expenditure as a share of GDP in 2021?  
**Filter người dùng:** None  
**Lý do thiếu evidence:** Box 2.2 (p30) chỉ nêu R&D intensity của Estonia (1,75%) và Poland (1,3%) năm 2021; với Bulgaria chỉ có tăng năng suất 1,4%/năm (bẫy gần nghĩa). grep 'Bulgaria' toàn văn: không có số R&D cho Bulgaria.  
**Queries:** ['Bulgaria R&D expenditure share of GDP 2021']  
**Context (3022 ký tự):** ['B:wdr2024_part1:p030:c001', 'B:wdr2024_part1:p031:c003', 'B:wdr2024_part1:p012:c002']  

**Trả lời:** The document does not contain enough evidence regarding Bulgaria's R&D expenditure as a share of GDP in 2021.

