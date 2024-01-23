# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 10:49:20 2024

@author: sea
"""

import streamlit as st
import random
import time
import pandas as pd 
class OralCalculation:  
    max_value=100  #最大整数
    min_value=5  #最小整数
    num_of_integer=2 #整数数量
    num_expression=10 #生成表达式数量
    showNo=True#显示题目序号
    problems = []
    answers = []
    
    def __init__(self,**kwargs):      
        self.config(**kwargs)
    def config(self,**kwargs):
        if 'max_value' in kwargs:
            self.max_value=kwargs['max_value']  #最大整数
        if 'min_value' in kwargs:
             self.min_value=kwargs['min_value']  #最小整数
        if 'num_of_integer' in kwargs:
            self.num_of_integer=kwargs['num_of_integer']  #整数数量
        if 'num_expression' in kwargs:
            self.num_expression=kwargs['num_expression']  #生成表达式数量
        if 'showNo' in kwargs:
            self.showNo=kwargs['showNo']  #显示题目序号
        if self.min_value>=self.max_value:
            raise ValueError("最小值应小于最大值！")     
    def getOperation(self):
        return ['+', '-', '*', '/'][random.randint(0, 1)]
        
    def generateIntegerExpression(self):
        # 确保至少有两个整数进行运算
        if self.num_of_integer < 2:
            raise ValueError("至少需要两个整数来生成四则运算表达式") 
        ops = [self.getOperation() for _ in range(self.num_of_integer-1)] 
        expression=""
        for i, op in enumerate(ops):
            if i==0:
                a=random.randint(self.min_value, self.max_value)
                expression=str(a)
                lastv=b=a
            while lastv==b:
                b=random.randint(self.min_value, self.max_value)
                
            if op=='-' and a<b:
                if a<self.min_value+1:
                    op='+'
                else:
                    b=random.randint(self.min_value, a-1)
            lastv=b

            expression+= f" {op} {b}"
           
            a=eval(expression)
        return expression, a
    def generate_batch_problems(self):
        self.problems = []
        self.answers = []
        expression=""
        for i in range(self.num_expression):
            while expression=="" or expression in self.problems:
                expression, result =self.generateIntegerExpression()   
            self.problems.append(expression)
            self.answers.append(result)  
        if self.showNo:  
            self.problems=[ f"{i}、 {s} =" for i, s in enumerate(self.problems, start=1)]
        return self.problems, self.answers
    def getproblems_answers(self):
        return self.problems, self.answers
 
def check_answers(show_cols):
    cralCalculation=st.session_state['cralCalculation']
    showByTable=st.session_state['showByTable']
    problems,correct_answers=cralCalculation.getproblems_answers()
    pSize=len(problems)
    if pSize<1:
        return
    score = 0 
    if not showByTable:
        checkanswers=st.session_state['checkanswers']
        answerBox=st.session_state['answerBox']
        for i, (problem, ca) in enumerate(zip(problems, correct_answers)):
          #  with st.expander(f"问题 {i+1}"):  # 使用Expander组件保持界面整洁
            abox=answerBox[i]
            if str(abox) == str(ca):
                score += 1
                checkanswers[i].info("✔️ 正确")
            else:
                checkanswers[i].error("✘ 错误，正确答案为："+str(ca))
    else:
        df=st.session_state.df
        de=st.session_state.de
        ipage=(pSize+show_cols-1)//show_cols
        for index, row in de.iterrows():
            for i in range(show_cols):
                if ipage*i+index>=pSize:
                    continue
                answerName=f'答案{i+1}'
                user_answer = row[answerName]
              #  user_answer
                correct_answer = correct_answers[ipage*i+index]
        
                if (user_answer) == str(correct_answer):
                    result = '✔'
                    score+=1
                else:
                    result = '✘ (正确答案: {})'.format(correct_answer)
        
                problemName=f'题目{i+1}'
                df.loc[df[problemName]==row[problemName],answerName]=user_answer
                df.loc[df[problemName]==row[problemName],f'结果{i+1}']=result 

        # 显示结果
        st.session_state.de=de
           
    accuracy = score / len(problems) * 100
    if score==len(problems):
        st.balloons()
    else:
        st.snow()
    correct_rate_str=f"\n正确率: {accuracy:.1f}%"
    st.session_state.correct_rate_str=correct_rate_str 
    st.toast(correct_rate_str)
def showproblems(colNum):
 
    cralCalculation=st.session_state['cralCalculation']
    showByTable=st.session_state['showByTable']
    problems,results=cralCalculation.getproblems_answers()
    pSize=len(problems)
    if pSize<1:
        return False
    if not showByTable:
        checkanswers=[]
        answerBox=[]
        cols = st.columns(colNum)    
        ipage=(pSize+colNum-1)//colNum
        for i, problem in enumerate(problems):
            k=i//ipage
            abox=cols[k].text_input(f"{problem}", value="",key=f"answer_input_{i}", placeholder="请输入答案...")    
            checkanswers.append(cols[k].empty())
            answerBox.append(abox)
            cols[k].write(' ')
     
        st.session_state['checkanswers']=checkanswers
        st.session_state['answerBox']=answerBox
    else: 
        dataholder= st.empty()
        bgenerate=st.session_state['btnGen1'] or st.session_state['btnGen2']or 'df' not in st.session_state
        if bgenerate:
            problems,results=cralCalculation.getproblems_answers() 
            ipage=(pSize+show_cols-1)//show_cols
            dfcoulumns={}
            disabledColumns=[]
            for i in range(show_cols):
               listp=problems[i*ipage:(i+1)*ipage] 
               listp.extend([''] * (ipage - len(listp)))
               dfcoulumns[f"题目{i+1}"]=listp
               dfcoulumns[f"答案{i+1}"]=""
               dfcoulumns[f"结果{i+1}"]="" 
             #  dfcoulumns[" "*(i+1)]="" 
               disabledColumns+=[f"题目{i+1}",f"结果{i+1}"]#," "*(i+1)
          #  st.write(dfcoulumns)
            df = pd.DataFrame(dfcoulumns)  # 使用pandas创建一个空答案列的DataFrame         
        else:
            df=st.session_state.df
            disabledColumns=st.session_state.disabledColumns 
    
        de=dataholder.data_editor(df,hide_index=True,
                      key="df_key", num_rows="fixed",disabled=tuple(disabledColumns))
        st.session_state.df=df
        st.session_state.de=de
        st.session_state.disabledColumns=disabledColumns
    return True


def start_stopwatch(running=True):
    if running:
        st.session_state.start_time = time.time()       
        st.session_state.elapsed_timeStr=""
        st.session_state.correct_rate_str=""
    else:
        elapsed_time = time.time() - st.session_state.start_time  
        elapsed_timeStr="耗时"+format_elapsed_time(elapsed_time)
        st.session_state.elapsed_timeStr = elapsed_timeStr
     #   st.write(format_elapsed_time(elapsed_time))
        st.toast(elapsed_timeStr)

def updateState():
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = 0 
        st.session_state['running'] = False 
        st.session_state['calcStatus']=True
        st.session_state['cralCalculation']=OralCalculation()
        st.session_state.elapsed_timeStr=""
        st.session_state.correct_rate_str=""
        
    isGenClick= ('btnGen1' in st.session_state and st.session_state['btnGen1'])or ( 'btnGen2' in st.session_state  and  st.session_state['btnGen2'])
    isFinClick=('btnFin1' in st.session_state and st.session_state['btnFin1'])or ( 'btnFin2' in st.session_state  and  st.session_state['btnFin2'])
    if isGenClick:        
        st.session_state['calcStatus']=not isGenClick
    if isFinClick:
        st.session_state['calcStatus']= isFinClick 
 #   st.write(f"calcStatus={st.session_state['calcStatus']}, isGenClick={isGenClick}, isFinClick={isFinClick} ")
def afterUpdateState(show_cols):
    isGenClick= ('btnGen1' in st.session_state and st.session_state['btnGen1'])or ( 'btnGen2' in st.session_state  and  st.session_state['btnGen2'])
    isFinClick=('btnFin1' in st.session_state and st.session_state['btnFin1'])or ( 'btnFin2' in st.session_state  and  st.session_state['btnFin2'])
    showByTable=st.session_state['showByTable']
    if isGenClick :        
        cralCalculation.generate_batch_problems()
        start_stopwatch()
    btnFin=False
    if not showByTable and  showproblems(show_cols): 
       btnFin= st.button('提交',key="btnFin2",disabled =calcStatus)     
    if isFinClick:
        check_answers(show_cols)
        start_stopwatch(False) 
    if showByTable and  showproblems(show_cols): 
        btnFin=st.button('提交',key="btnFin2",disabled =calcStatus) or  btnFin     
   # st.write(f"btnFin={btnFin}")
    correct_rate_str = st.session_state.correct_rate_str
    if correct_rate_str:
        st.write(correct_rate_str)
    elapsed_timeStr = st.session_state.elapsed_timeStr
    if elapsed_timeStr:
        st.write(elapsed_timeStr)
    
def format_elapsed_time(elapsed_seconds):
    hours = elapsed_seconds // 3600
    remaining_seconds = elapsed_seconds % 3600
    minutes = remaining_seconds // 60
    seconds = remaining_seconds % 60

    time_string = []
    if hours > 0:
        time_string.append(f"{hours} 小时")
    if minutes > 0 or (hours > 0 and seconds > 0):  # 如果有小时且还有剩余秒数，即使分钟为0也显示
        time_string.append(f"{minutes} 分钟")
    time_string.append(f"{seconds:.1f} 秒")

    return " ".join(time_string)
if __name__ == "__main__":    
    # 设置页面配置，其中 `page_width` 可以是 'normal', 'wide', 或者一个自定义像素值（整数）
    st.set_page_config(layout="wide", page_title="口算练习", page_icon="🦈")
   # st.title('口算练习')


    
    updateState()
    
    calcStatus= st.session_state['calcStatus']         
    cralCalculation=st.session_state['cralCalculation']
    
    st.button('生成',key="btnGen2",disabled =not calcStatus)
    with st.sidebar:
        st.toggle('表格显示',key="showByTable")
        num_problems = st.slider("请选择题目数量（例如：20）", value=20,min_value=10, max_value=50,step=5) 
        max_value = st.slider("请选择最大值（例如：10）", value=25,min_value=10, max_value=100,step=5) 
        min_value = st.slider("请选择最小值（例如：1）", value=5,min_value=1, max_value=max_value-1,step=1)         
        show_cols = st.slider("请选择显示列数（例如：2）", value=3,min_value=1, max_value=5)  
        num_of_integer = st.slider("请选择运算项数（例如：2）", value=2,min_value=2, max_value=10) 
        cralCalculation.config(num_of_integer=num_of_integer,max_value=max_value,min_value=min_value,num_expression=num_problems)
        cols = st.columns(2)
        cols[0].button('生成',key="btnGen1",disabled =not calcStatus)
        cols[1].button('提交',key="btnFin1",disabled =calcStatus) 
 
    afterUpdateState(show_cols)
 