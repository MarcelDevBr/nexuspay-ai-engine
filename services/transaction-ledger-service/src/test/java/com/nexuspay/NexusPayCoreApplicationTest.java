package com.nexuspay;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertNotNull;

class NexusPayCoreApplicationTest {

    @Test
    void testContextLoads() {
        NexusPayCoreApplication app = new NexusPayCoreApplication();
        assertNotNull(app);
    }
}
