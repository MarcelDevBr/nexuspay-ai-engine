package com.nexuspay.infrastructure.config;

import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;
import software.amazon.awssdk.services.sqs.SqsClient;

import static org.junit.jupiter.api.Assertions.assertNotNull;

class AwsSqsConfigTest {

    @Test
    void testSqsClientBeanCreation() {
        AwsSqsConfig config = new AwsSqsConfig();
        ReflectionTestUtils.setField(config, "region", "us-east-1");
        ReflectionTestUtils.setField(config, "endpointUrl", "http://localhost:4566");

        SqsClient client = config.sqsClient();
        assertNotNull(client);
    }
}
