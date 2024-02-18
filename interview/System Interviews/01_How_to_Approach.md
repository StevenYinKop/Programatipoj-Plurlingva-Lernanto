# How to Approach

> Scoping the questions
> Don't over-engineer
> Clarify main questions at the beginning in case of having no time to change something during the interview.

[//]: # (Aroch)

## Can you take feedback from me? How do you respond to my direction? How do you work well with me?

## Start by Clarifying Requirements:
- Repeat the question back to the interviewer. -> Make sure that you understand it properly.
- **Think out loud**. Don't just sit there in silence.

### Working Backwards
> Start from the customer experience to define your requirements
- Identify WHO are the customers.
- WHAT are their use cases.
- WHICH use cases do you need to concern yourself with
  - You're not going to design all of YouTube in 20 minutes.
- Your initial task is to CLARIFY THE REQUIREMENTS of what you are designing
- Your interviewer wants to see that you can think about problems from a business perspective and not a purely technical one.

### Defining Scaling Requirements

### Defining Latency Requirements

### Defining Availability Requirements



### Functional
  - Clarify with interviewers in general
### Non-Functional
  - Scalability: Single Database can't handle 100M Daily Active User(DAU)
  - Availability: non error rate (99.999% 20minutes downtime per year) 
  - Though put:
  - Storage Capacity:
  - Performance:
      - Latency
      - Partition
      - Read to be fast(less than 1s), more tolrant on writing

## Back of the envelope Calculations

100M DAU
1. 10B reads
2. 10M writes

Through Put = 10b / 86400(second in a day) = 100,000 reads/sec, 100 writes/sec

1s = 1000 ms = 1,000,000 microsecond = 1,000,000,000 nanoseconds


## Database
schema: SQL/NoSQL
scale/single instance db


