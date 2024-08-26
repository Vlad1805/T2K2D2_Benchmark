-- top-K keywords TFIDF by gender - ok
with
    noDocs as (select distinct id_document 
                from document_facts f 
                inner join author_dimension ad 
                on ad.id_author = f.id_author
                where gender='male'
                )
    select wd.word, sum(f.tf) * (1+(select count(id_document) from noDocs)/count(distinct f.id_document)) TFIDF
    from 
        document_facts f
        inner join author_dimension ad on ad.id_author = f.id_author
        inner join word_dimension wd on wd.id_word = f.id_word
    where
        ad.gender = 'male'
    group by wd.word
    order by 2 desc
    limit 10;
