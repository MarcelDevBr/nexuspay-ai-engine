# Standalone Dockerfile for Transaction Ledger Service (Java 26 / Spring Boot 4)
FROM eclipse-temurin:26 AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends curl unzip && rm -rf /var/lib/apt/lists/*

COPY pom.xml mvnw ./
COPY .mvn ./.mvn

RUN chmod +x mvnw && ./mvnw dependency:resolve -B || true

COPY src ./src
RUN ./mvnw clean package -DskipTests

# Stage de Produção
FROM eclipse-temurin:26-jre AS runner

WORKDIR /app

RUN useradd -m -u 1001 spring
USER spring:spring

COPY --from=builder /app/target/*.jar app.jar

EXPOSE 8081

ENTRYPOINT ["java", "-XX:+UseZGC", "-XX:+ZGenerational", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
