-- top-K keywords  TFIDF by gender & date - ok
with
    noDocs as (select distinct id_document 
                from document_facts f 
                    inner join author_dimension ad on ad.id_author = f.id_author
                    inner join time_dimension td on td.id_time = f.id_time
                where ad.gender='female'
                    and td.full_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00'
                )
select wd.word, sum(f.tf) * (1+(select count(id_document) from noDocs)/count(distinct f.id_document)) TFIDF
    from 
        document_facts f
        inner join time_dimension td on td.id_time = f.id_time
        inner join author_dimension ad on ad.id_author = f.id_author
        inner join word_dimension wd on wd.id_word = f.id_word
    where
        ad.gender = 'female'
        and td.full_date between '2015-09-17 00:00:00' and '2015-09-18 00:00:00'
    group by wd.word
    order by 2 desc
    limit 10;