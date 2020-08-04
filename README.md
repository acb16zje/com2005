# Bio-Computing
| Section | Comments | Mark |
|-------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|
| Abstract and Introduction | Abstract covers general features of model but specific client problem is not introduced. This could have been mentioned earlier in the Introduction section. | 6/10 |
| Literature Review | Good brief introduction to historic development Cellular Automata and an overview of some existing models, including non-CA approaches and their primary findings. You could have commented on advantages/disadvantages of different approaches or mentioned issues of parameterisation of these models. | 15/20 |
| Model Description/Methodology | Good attempt to relate your assumptions of behaviour and parameters to the literature. Good use of figures to communicate methodology though I would have liked to see a ‘per cell’ flow/decision chart in place of figure 2 (e.g. if cell is not on fire  is any neighbour on fire…..). Parameter values could have been tabulated. Provided terrain map is not included and how you have incorporated the effect of water is not mentioned. | 14/20 |
| Code, simulations and results | You have explored effect of wind speed on relative time to reach town with clear presentation of results. I am slightly confused as to whether the behaviour shown in Results figure 2 is reasonable as imposing wind from north should surely increase fire spread to south? The time points on this figure are not stated. It is difficult to interpret figure 3 as there is no quantitative explanation of results. Long term intervention is clearer. No indication that repeat simulations were run to account for stochasticity, though this is touched upon in your discussion. Code is functional , well commented and a readme file supplied. | 13/20 |
| Discussion and Conclusion | I can’t relate your “5 and 10 day” figure stated at the start of this section with the results presented in your previous tables (though the “relative” time that you were asked for does agree. You have not dedicated much discussion to the questions posed by the client, but your wider discussion of the realism, limitations and possible improvements to your model is very good, as is your attempts to compare your approach to published work. | 16/20 |
| Presentation | Well written with good standard of English and generally clear and concise descriptions. Good use of figures, though some double labelling (i.e. you have two figure 1’s and figure 2’s). Colour keys should be included with complete information in captions. Good consistent referencing style and within specified page limit. Code elegance could have ben improved by eliminating unused imports and commented out instructions, using consistent variable naming conventions and separating | 7/10 |
| Total |  | 71% |

# Robotics
| Questions | Feedback | Credit | Mark |
|-----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|------|
| Q1 | When you explain different terms it is important to add examples. | 1 | 2 |
| Q2 |  | 2 | 2 |
| Q3 |  | 4 | 4 |
| Q4 | There are not clear what happen when rb or how e = r - b works in your example. | 4 | 8 |
| Q5 |  | 4 | 4 |
| Q6 | Well explained both cases. But, you mentioned that the maximum range of the sensor are around 1.7m, why not add those values in the table and only tested between 1 cm and 15 cm. Also, you should be consistent in the measure units. If you show the real distance in CM, the sensor reading should be in the same unit and not in meters. This change of units can lead to a misreading of the values. Additionally, if you are showing a mean value you should add this keyword somewhere and add other statistics values like max, min, std var, number of samples, | 7 | 8 |
| Q7 |  | 2 | 2 |
| Q8 | A nice table explaining behaviour at different Kp values is a good way to show and record how you found your 'good' value | 4 | 5 |
| Q9 | You explain that Ku is bigger than Kp but no a specific relation ( Kp=Ku/2 ). It was asked for your Ku value. I found it in another question but not here where was requested. | 3 | 5 |
| Q10 |  | 5 | 5 |
| Q11 | The units in your table it is not suitable, working in sec when all the values are below zero is a clear indication that you should work in msec. You tested values are to high, started with 100 msec (0.1 sec) is a very high value when the default one is close to 1msec (0.001sec). You didn't see the behaviour with, for example, reading every 50 msec. | 2 | 5 |
| Q12 |  | 5 | 5 |
| Q13 |  | 17.5 | 20 |
| Q14 | Well done. Very good explanation about what did you explore and your results. | 15 | 15 |
| Q15 |  | 5 | 5 |
| Q16 | The material of the wall doesn't really affect as the sensors are ultrasonic. | 1 | 5 |
| **Total** |  | **81.5** | **100** |