import sparknlp
from sparknlp.base import DocumentAssembler, Pipeline
from sparknlp.annotator import SentimentDetector, ViveknSentimentApproach

class SparkProcessor:
    """Apache Spark for data processing and ML"""

    def __init__(self):
        self.spark = None
        self.sentiment_pipeline = None
        self.initialize_spark()

    def initialize_spark(self):
        """Initialize Spark Session with Spark NLP"""
        try:
            # Check if Java is available
            import subprocess
            java_check = subprocess.run(['java', '-version'],
                                       capture_output=True,
                                       text=True,
                                       timeout=5)

            if java_check.returncode != 0:
                raise Exception("Java not found")

            self.spark = sparknlp.start()
            print("Spark initialized with Spark NLP")

            # Try to load pre-trained sentiment model
            try:
                document = DocumentAssembler() \
                    .setInputCol("text") \
                    .setOutputCol("document")

                sentiment = SentimentDetector.pretrained() \
                    .setInputCols(["document"]) \
                    .setOutputCol("sentiment")

                self.sentiment_pipeline = Pipeline(stages=[document, sentiment])
                print("Spark NLP sentiment model loaded")

            except:
                print("Spark NLP pre-trained model not available, using VADER")

        except Exception as e:
            print(f"Spark not available (using pandas fallback): {str(e)[:50]}")
            self.spark = None

    def process_with_spark(self, data, data_type):
        """Process data using Spark"""
        if self.spark is None:
            # Fallback to pandas
            return data

        try:
            # Convert to Spark DataFrame
            if data_type == 'news':
                df = self.spark.createDataFrame(data)
            elif data_type == 'tweets':
                df = self.spark.createDataFrame(data)
            else:
                df = self.spark.createDataFrame(data)

            print(f"Processed {df.count()} records with Spark")
            return df.toPandas()

        except Exception as e:
            print(f"Spark processing failed (using pandas): {e}")
            return data

    def stop(self):
        """Stop Spark session"""
        if self.spark:
            try:
                self.spark.stop()
            except:
                pass
