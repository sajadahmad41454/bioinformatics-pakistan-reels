import soundfile as sf, json, os
from kokoro_onnx import Kokoro
M=os.environ.get("KOKORO_DIR","./")
k=Kokoro(M+"kokoro-v1.0.onnx",M+"voices-v1.0.bin")
lines=[
"Tuberculosis, or TB, is caused by a bacterium called Mycobacterium tuberculosis.",
"And Pakistan is among the countries with the most TB cases in the world.",
"It spreads through the air when a person with lung TB coughs, sneezes, or spits.",
"About a quarter of the world's population is estimated to have been infected.",
"But most never fall ill. The immune system keeps the bacteria in check. This is latent TB, and it does not spread to others.",
"Infected people have a five to ten percent lifetime risk of TB disease, higher if the immune system is weak.",
"TB most often affects the lungs, with a long-lasting cough, fever, night sweats, and weight loss.",
"WHO recommends rapid molecular tests as the first test.",
"Some TB bacteria resist the standard drugs, and drug-resistant TB needs longer, more complex treatment.",
"Bioinformatics helps here. Sequencing the bacterial genome reveals mutations linked to drug resistance.",
"And a WHO catalogue helps labs interpret those mutations, for thirteen TB medicines.",
"So if a cough lasts three weeks or more, get tested, and see a doctor.",
]
os.makedirs("v_tb",exist_ok=True); durs=[]
for i,l in enumerate(lines):
    a,sr=k.create(l,voice="af_heart",speed=0.95,lang="en-us")
    sf.write(f"v_tb/l{i}.wav",a,sr); durs.append(round(len(a)/sr,2))
json.dump({"v_tb":{"lines":lines,"durs":durs,"sr":sr}},open("tts.json","w"),indent=1)
print(durs,round(sum(durs),1), round(sum(durs)+0.3*11+0.4+2.6,1))
