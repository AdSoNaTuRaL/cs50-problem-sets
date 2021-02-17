-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Ler as logs de crime na cidade no dia do roubo
SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28;

-- Ler as entrevistas feitas com as testemunhas no dia do roubo
SELECT * FROM interviews WHERE month = 7 AND day = 28;

-- Ver as logs de seguranca do tribunal no dia do roubo e que a atividade seja saida
SELECT * FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND activity = "exit";

-- Ver as transacoes feitas no dia do Roubo na rua mencionada pela testemunha Eugene com o tipo
-- de transacao retirada
SELECT * FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street"
AND transaction_type = "withdraw";

-- Vejo o id de todas as pessoas que tem contas de numero que coincidam com as transcoes de retirada
-- feitas naquele dia
SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street"
AND transaction_type = "withdraw");

-- vejo informacoes de todas as pessoas que fizeram algum tipo de transacao bancaria no caixa eletronico
-- no dia do roubo
SELECT p.license_plate FROM people p WHERE p.id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street"
AND transaction_type = "withdraw"));

-- Faco um filtro nas placas que sairam no dia do roubo
SELECT license_plate FROM courthouse_security_logs WHERE month = 7 AND day = 28 AND activity = "exit" AND
license_plate IN (SELECT p.license_plate FROM people p WHERE p.id IN (SELECT person_id FROM bank_accounts WHERE account_number IN
(SELECT account_number FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = "Fifer Street"
AND transaction_type = "withdraw")));

-- Output 94KL13X, 4328GD8, L93JTIZ, 322W7JE, 1106N58

-- Informacoes das pessoas que tem as placas de carro suspeitas
SELECT * FROM people WHERE license_plate IN ('94KL13X', '4328GD8', 'L93JTIZ', '322W7JE', '1106N58');

-- Aqui eu pego o numero de telefone de todos os suspeitos
SELECT phone_number FROM people WHERE license_plate IN ('94KL13X', '4328GD8', 'L93JTIZ', '322W7JE', '1106N58');

-- Aqui eu pego o registro de chamadas que duraram menos de 1 minuto
-- de todos os suspeitos no dia do crime
SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND caller IN
(SELECT phone_number FROM people WHERE license_plate IN
('94KL13X', '4328GD8', 'L93JTIZ', '322W7JE', '1106N58')) AND duration < 60;

-- Id do aeroporto que eles sairam (origem) -- OUTPUT 8
SELECT id FROM airports WHERE city = "Fiftyville";

-- Pego o voo que sai mais cedo do aeroporto de Fiftyville um dia apos o roubo
-- Id do voo 36
SELECT min(hour) as "Early fly", * FROM flights WHERE origin_airport_id = 8 AND day = 29 AND month = 7;

-- Qual aeroporto de destino - London Heathrow Airport
SELECT * FROM airports WHERE id = 4;

-- Descubro o passaporte dos suspeitos que coincidem com o id do voo
SELECT passport_number FROM passengers WHERE flight_id = 36 AND passport_number IN
(SELECT passport_number FROM people WHERE license_plate IN ('94KL13X', '4328GD8', 'L93JTIZ', '322W7JE', '1106N58'));

-- Descubro as pessoas que compraram passagem
-- de voo no dia apos o roubo, atraves do numero de passaporte e das chamadas feitas pelos suspeitos
SELECT * FROM people WHERE passport_number IN (SELECT passport_number FROM passengers WHERE flight_id = 36 AND passport_number IN
(SELECT passport_number FROM people WHERE license_plate IN ('94KL13X', '4328GD8', 'L93JTIZ', '322W7JE', '1106N58'))
AND phone_number IN
(SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND caller IN
(SELECT phone_number FROM people WHERE license_plate IN
('94KL13X', '4328GD8', 'L93JTIZ', '322W7JE', '1106N58')) AND duration < 60));

-- saber as chamadas dos dois possiveis suspeitos
SELECT * FROM phone_calls WHERE caller IN ("(286) 555-6063", "(367) 555-5533") AND day = 28 AND duration < 60;

-- Hora do roubo 10am

-- Saber os possiveis cumplices do crime
SELECT * FROM people where phone_number IN
(
SELECT receiver FROM phone_calls WHERE caller IN ("(286) 555-6063", "(367) 555-5533") AND day = 28 AND duration < 60
);

-- Saber a placa do carro dos possiveis cumplices
SELECT license_plate FROM people where phone_number IN
(
SELECT receiver FROM phone_calls WHERE caller IN ("(286) 555-6063", "(367) 555-5533") AND day = 28 AND duration < 60
);

-- Verifico se os possiveis cumplices estavam no tribunal no dia do roubo,
-- porque eh impossivel ja que estaria em outro lugar, comprando as passagens
SELECT * FROM courthouse_security_logs WHERE day = 28 and activity = "exit"
and license_plate in (SELECT license_plate FROM people where phone_number IN
(
SELECT receiver FROM phone_calls WHERE caller IN ("(286) 555-6063", "(367) 555-5533") AND day = 28 AND duration < 60
));

-- Ha dois suspeitos como cumplice, mas so um estava no tribunal no dia do crime
select * from people where license_plate = "4V16VO0";
-- 864400 | Berthold | (375) 555-8161 |  | 4V16VO0

-- descubro o criminoso
SELECT * FROM people WHERE phone_number = (
SELECT caller FROM phone_calls WHERE receiver = "(375) 555-8161" and day = 28
);

-- 686048 | Ernest | (367) 555-5533 | 5773159633 | 94KL13X


