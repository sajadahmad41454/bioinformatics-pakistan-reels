import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"Dengue is a viral infection spread by mosquitoes, and a familiar threat in Pakistan.",
"It spreads through the bite of an infected Aedes mosquito, mainly Aedes aegypti.",
"These mosquitoes bite during the day, both indoors and outdoors.",
"And they lay their eggs in stagnant water around our homes.",
"Most infections are mild, or cause no symptoms at all.",
"Symptoms usually start four to seven days after the bite: a sudden high fever, headache, and muscle and joint pain.",
"There are four types of dengue virus, called serotypes one to four.",
"One infection gives long-term protection against that type, but not the others.",
"And a second infection with a different type carries a greater risk of severe dengue.",
"There is no specific antiviral drug, so treatment is supportive.",
"Labs can confirm dengue with an NS1 antigen test, or RT-PCR.",
"Bioinformatics helps too. Sequencing the viral genome identifies serotypes, and tracks how outbreaks spread.",
"So, empty stagnant water, use repellent, and cover up during the day.",
"And if you get a high fever, see a doctor early.",
]
os.makedirs("v_dengue",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.95,lang="en-us")
    sf.write(f"v_dengue/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
json.dump({"v_dengue":{"lines":lines,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.3*13+0.4+2.6,1))
