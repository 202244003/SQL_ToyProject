CREATE SCHEMA hairsalon;

USE hairsalon;

# 고객 테이블
CREATE TABLE customer (
	customer_id INT AUTO_INCREMENT PRIMARY KEY,	-- 고객 번호
    name VARCHAR(100) NOT NULL,					-- 고객 이름
    phone VARCHAR(20) NOT NULL,					-- 연락처
    gender ENUM('F', 'M') NOT NULL,				-- 성별
    birth_date DATE,							-- 생년월일
    memo TEXT,									-- 고객 메모
    points INT DEFAULT 0,						-- 보유 포인트
    grade ENUM('일반', '단골', 'VIP') DEFAULT '일반' -- 고객 등급
);

# 시술 테이블
CREATE TABLE service (
	service_id INT AUTO_INCREMENT PRIMARY KEY, 	-- 시술 번호
    service_name VARCHAR(100) NOT NULL,			-- 시술 이름
    price INT NOT NULL,				-- 가격
    service_detail TEXT 						-- 시술 설명
); 

# 방문 테이블
CREATE TABLE visit (
	visit_id INT AUTO_INCREMENT PRIMARY KEY,	-- 방문 번호
	customer_id INT NOT NULL,					-- 고객 번호
    visit_date DATETIME NOT NULL,				-- 방문 날짜
    note TEXT									-- 방문 메모
);

# 방문 상세 테이블
CREATE TABLE visit_detail (
	visit_id INT NOT NULL,						-- 방문 번호
    service_id INT NOT NULL,					-- 시술 번호
    PRIMARY KEY (visit_id, service_id)
);

# 결제 테이블
CREATE TABLE payment (
	payment_id INT AUTO_INCREMENT PRIMARY KEY,	-- 결제 번호
    visit_id INT NOT NULL,						-- 방문 번호
    amount INT NOT NULL,				-- 금액
    method ENUM('현금', '카드', '포인트') NOT NULL	-- 결제 방식
);

# 방문 테이블 - 고객(고객 번호) FK
ALTER TABLE visit
ADD CONSTRAINT fk_visit_customer
FOREIGN KEY (customer_id)
REFERENCES customer(customer_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

# 방문 상세 테이블 - 방문(방문 번호) FK
ALTER TABLE visit_detail
ADD CONSTRAINT fk_visit_visit_detail
FOREIGN KEY (visit_id)
REFERENCES visit(visit_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

# 방문 상세 테이블 - 시술(시술 번호) FK
ALTER TABLE visit_detail
ADD CONSTRAINT fk_visit_detail_service
FOREIGN KEY (service_id)
REFERENCES service(service_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

# 결제 테이블 - 방문(방문 번호) FK
ALTER TABLE payment
ADD CONSTRAINT fk_payment_visit
FOREIGN KEY (visit_id)
REFERENCES visit(visit_id)
ON DELETE CASCADE
ON UPDATE CASCADE;


