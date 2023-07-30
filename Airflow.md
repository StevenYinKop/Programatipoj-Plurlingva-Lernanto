---
title: Airflow
url: https://www.yuque.com/stevenyin/liv/tugd0ok0zev94n65
---

<a name="rQ9qj"></a>

## DAG

<a name="FsLIh"></a>

### Steps of Defining DAG

1. Instantiating a DAG object
2. Implementing Tasks with Operators.
3. Adding dependencies between Tasks. <a name="UiDDt"></a>

### Important Properties

`dag_id` unique identifier of your DAG.
`description` the description of your DAG.
`start_date` indicates from which date your DAG should start.
`schedule_interval` defines how often your DAG runs from the start\_date.
`default_args` a dictinary containing parameters that will be applied to all operators and so to your tasks.
`catchup` to perform scheduler catchup (True by default).
