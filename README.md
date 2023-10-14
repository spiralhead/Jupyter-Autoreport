# Jupyter-Autoreport
Пример автоматически собираемых отчетов для Jupyter Notebook
## Установка
Пример собирался с помощью conda environment, поэтому python лучше использовать из [Anaconda/Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/windows.html). Можно использовать и обычный Python>=3.10, но кнопку генерации кода тогда надо будет переделать самостоятельно.
Также требуется установить [MiKTeX](https://miktex.org/download).
После установки, необходимо запустить Anaconda Prompt и установить cреду из файла env.yml
~~~
conda env create -f env.yml
~~~
Установка среды может занять продолжительное время.После установки необходимо среду активировать, и запустить Jupyter Notebook
~~~
conda activate test_autodoc
jupyter lab
~~~
## Использование
Если все установлено нормально, для генерации отчета достаточно открыть один из ipynb файлов в Jupyter Notebook/Lab (Lab тоже есть в поставке); запустить первую ячейку и вывести кнопку генерации отчета;нажать на кнопку, и запустить генерацию отчета.