#!/usr/bin/env bash

py_dir=../src/python

pyexec='python'
unamestr=`uname`
if [[ "$unamestr" == 'Linux' ]]; then
   pyexec='python3'
fi

#model_dir=model_dir:${1}
#num_topics=num_topics:${2}
#${pyexec} ${py_dir}/utils/lda_team_builder ${model_dir} ${num_topics}

#Samples
echo "Generating for samples..."
num_topics=num_topics:10
model_dir=model_dir:full/samples
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}

model_dir=model_dir:ally/samples
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}

model_dir=model_dir:enemy/samples
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}

model_dir=model_dir:offender/samples
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}

#Full models
echo "Generating for full models..."
model_dir=model_dir:full
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}

model_dir=model_dir:ally
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}

model_dir=model_dir:enemy
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}

model_dir=model_dir:offender
${pyexec} ${py_dir}/utils/lda_team_builder.py ${model_dir} ${num_topics}