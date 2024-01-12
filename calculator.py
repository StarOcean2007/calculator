# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 10:49:20 2024

@author: sea
"""

import streamlit as st
import random
import time

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
            self.problems.append(f"{i+1}、 {expression} ="  if self.showNo else expression)
            self.answers.append(result)  
        return self.problems, self.answers
    def getproblems_answers(self):
        return self.problems, self.answers
 
def check_answers():
    cralCalculation=st.session_state['cralCalculation']
    problems,correct_answers=cralCalculation.getproblems_answers()
    pSize=len(problems)
    if pSize<1:
        return
    score = 0
    start_time = time.time() 
 
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
    accuracy = score / len(problems) * 100
    if score==len(problems):
        st.balloons()
    else:
        st.snow()

    st.write(f"\n正确率: {accuracy:.2f}%") 
    st.toast(f"\n正确率: {accuracy:.2f}%")
def showproblems(colNum):
 
    cralCalculation=st.session_state['cralCalculation']
    problems,results=cralCalculation.getproblems_answers()
    pSize=len(problems)
    if pSize<1:
        return
    checkanswers=[]
    answerBox=[]
    # problemsPart=st.empty()
    # with problemsPart.container():
    cols = st.columns(colNum)
    
    ipage=(pSize+colNum-1)//colNum
    for i, problem in enumerate(problems):
        k=i//ipage
        abox=cols[k].text_input(f"{i+1}、  {problem} =", value="",key=f"answer_input_{i}", placeholder="请输入答案...")    
        checkanswers.append(cols[k].empty())
        answerBox.append(abox)
        cols[k].write(' ')
 
    st.session_state['checkanswers']=checkanswers
    st.session_state['answerBox']=answerBox
        


def start_stopwatch():
    if not st.session_state.running:
        st.session_state.start_time = time.time()
        st.session_state.running = True
    else:
        elapsed_time = time.time() - st.session_state.start_time 
        st.session_state.running = False
        st.session_state.start_time = 0 
        st.session_state.elapsed_time=elapsed_time  
        st.write(f"已计时：{elapsed_time:.2f} 秒", key='stopwatch')
        st.toast(f"已计时：{elapsed_time:.2f} 秒")
 

if __name__ == "__main__":    
    # 设置页面配置，其中 `page_width` 可以是 'normal', 'wide', 或者一个自定义像素值（整数）
    st.set_page_config(layout="wide", page_title="口算练习", page_icon="calculator")
    # 页面布局
   # st.title('口算练习')
    # 初始化秒表状态
    if 'start_time' not in st.session_state:
        st.session_state['start_time'] = 0
        st.session_state['stopwatch'] = 0
        st.session_state['running'] = False
    
    if 'cralCalculation' not in st.session_state:
        st.session_state['cralCalculation']=OralCalculation()
    cralCalculation=st.session_state['cralCalculation']
    with st.sidebar:
        num_problems = st.slider("请选择题目数量（例如：20）", value=20,min_value=10, max_value=50,step=5) 
        max_value = st.slider("请选择最大值（例如：10）", value=10,min_value=10, max_value=100,step=5) 
        min_value = st.slider("请选择最小值（例如：1）", value=5,min_value=1, max_value=100,step=1)         
        show_cols = st.slider("请选择显示列数（例如：2）", value=3,min_value=1, max_value=5)  
        num_of_integer = st.slider("请选择运算项数（例如：2）", value=2,min_value=2, max_value=10) 
        cralCalculation.config(num_of_integer=num_of_integer,max_value=max_value,min_value=min_value,num_expression=num_problems)
        cols = st.columns(4)
        btn1=cols[1].button('生成')
        btn2=cols[2].button('提交')
    if btn1:  
        cralCalculation.generate_batch_problems()
        start_stopwatch()
    showproblems(show_cols)
    
    if btn2:  
        check_answers()
        start_stopwatch()