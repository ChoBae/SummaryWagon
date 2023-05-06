from fastapi import APIRouter
from app.routers.preprocess import word_preprocess
import httpx
import json
import time 

# from ..models.article import Article
from ..database import (
    get_hot_articles,
)

router = APIRouter(
    prefix="/articles",
    tags=["articles"],
)

# url
url = "https://techblog.woowahan.com/11072/"
lambda_url = 'https://xb8gag6ij9.execute-api.ap-northeast-2.amazonaws.com/default/openai_invoke_api'

data = {"contents" : '''Speakers ranging from artificial intelligence (AI) developers to law firms grappled this week with questions about the efficacy and ethics of AI during MIT Technology Review's EmTech Digital conference. Among those who had a somewhat alarmist view of the technology (and regulatory efforts to rein it in) was Tom Siebel, CEO C3 AI and founder of CRM vendor Siebel Systems.

Siebel was on hand to talk about how businesses can prepare for an incoming wave of AI regulations, but in his comments Tuesday he touched on various facets of the debate of generative AI, including the ethics of using it, how it could evolve, and why it could be dangerous.

For about 30 minutes, MIT Technology Review Editor-in-Chief Mat Honan and several conference attendees posed questions to Siebel, beginning with what are the ethical and unethical uses of AI. The conversation quickly turned to AI’s potential to cause damage on a global scale, as well as the nearly impossible task of setting up guardrails against its use for unintended and intended nefarious purposes.

[ Related: How AI is helping the help desk ]
The following are excerpts from that conversation.

[Honan] What is ethical AI, what are ethical uses of AI or even unethical uses of AI? "The last 15 years we’ve spent a couple billion dollars building a software stack we used to design, develop, provision, and operate at massive scale enterprise predictive analytics applications. So, what are applications of these technologies I where I don’t think we have to deal with bias and we don’t have ethical issues?

"I think anytime we’re dealing with physical systems, we’re dealing with pressure, temperature, velocity, torque, rotational velocity. I don’t think we have a problem with ethics. For example, we’re…using it for one of the largest commercial applications for AI, the area of predictive maintenance.

"Whether it’s for power generation and distribution assets in the power grid or predictive maintenance for offshore oil rigs, where the data are extraordinarily large data sets we’re arriving at with very rapid velocity, ...we’re building machine-learning models that are going to identify device failure before it happens — avoiding a failure of, say, an offshore oil rig of Shell. The cost of that would be incalculable. I don’t think there are any ethical issues. I think we can agree on that.

[ REGISTER NOW for May 11, in-person event, FutureIT Washington, D.C.: Building the Digital Business with Cloud, AI and Security ]
"Now, anytime we get to the intersection of artificial intelligence and sociology, it gets pretty slippery, pretty fast. This is where we get into perpetuating cultural bias. I can give you specific examples, but it seems like it was yesterday — it was earlier this year — that this business came out of generative AI. And is generative AI an interesting technology? It’s really an interesting technology. Are these large language models important? They’re hugely important.

"Now all of a sudden, somebody woke up and found, gee, there are ethical situations associated with AI. I mean, people, we’ve had ethical situations with AI going back many, many years. I don’t happen to have a smartphone in my pocket because they striped it from me on the way in, but how about social media? Social media may be the most destructive invention in the history of mankind. And everybody knows it. We don’t need ChatGPT for that.

"So, I think that’s absolutely an unethical application of AI. I mean we’re using these smartphones in everybody’s pocket to manipulate two to three billion people at the level of the limpid brain, where we’re using this to regulate the release of dopamine. We have people addicted to these technologies. We know it causes an enormous health problem, particularly among young women. We know it causes suicide, depression, loneliness, body image issues – documented. We know these systems are the primary exchange for the slave trade in the Middle East and Asia. These systems call in to question our ability to conduct a free and open Democratic society.

"Does anyone have an ethical problem with that? And that’s the old stuff. Now we get into the new stuff."

Siebel spoke about government requests made of his company. "Where have I [seen] problems that we’ve been posed? OK. So, I’m in Washington DC. and I won’t say in whose office or what administration, but it’s a big office. We do a lot of work in the Beltway, in things like contested logistics, AI predictive maintenance for assets in the United States Air Force, command-and-control dashboards, what have you, for SOCOM [Special Operations Command], TransCom [Transportation Command], National Guard, things like this.

"And, I’m in this important office and this person turns his office over to his civilian advisor who’s a PhD in behavioral psychology…, and she starts asking me these increasingly uncomfortable questions. The third question was, ‘Tom, can we use your system to identify extremists in the United States population.’

"I’m like holy moly; what’s an extremist? Maybe a white male Christian? I just said, 'I’m sorry, I don’t feel comfortable with this conversation. You’re talking to the wrong people. And this is not a conversation I want to have.' Now, I have a competitor who will do that transaction in a heartbeat.

'''}

@router.get("/")
async def read_hot_articles():
    hot_articles = await get_hot_articles()
    return hot_articles
 
 
"""article parsing """
@router.get("/details", response_description="")
async def crawling_articles():
    result = word_preprocess(url)
    
    print(result)
    
    return True


@router.get("/lambda")
async def lambda_request():
    start_time = time.time()
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/json", "Accept-Encoding" : "gzip, deflate, br"}
    
        timeout = httpx.Timeout(300.0, read=None)    
        
        flag = False
        
        # while (flag == False):
        r = httpx.post(lambda_url, headers=headers, data = data, timeout = timeout)         
        print(r.text)
            
            # if (txt['message'] == None):
            #     flag = True 
            
        print("--- %s seconds ---" % (time.time() - start_time))
        
    
    
    
        # response = await client.get(url)
        # response = await client.put(lambda_url, data = data1)
        
        # print(type(response))
        # print(response.text)
        # print(response.decode("utf-8"))
        
        # print(response.json())
        
        # trace_json = json.loads(response.json().replace(b"\\", b" "), strict=False)
        
        # print(trace_json)    
    
    return 1