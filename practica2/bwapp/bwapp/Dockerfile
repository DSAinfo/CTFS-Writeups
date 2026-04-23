FROM raesene/bwapp

RUN sed -i  's/$xml = simplexml_load_string($body);/ $xml = simplexml_load_string($body,'SimpleXMLElement', LIBXML_NOENT);/' /app/xxe-2.php
