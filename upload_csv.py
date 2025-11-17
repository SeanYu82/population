"""
CSV 파일을 Supabase에 업로드하는 스크립트
사용법: python upload_csv.py
"""
import csv
import os
from supabase import create_client, Client

# Supabase 설정
SUPABASE_URL = "https://gkklkjoatvbxfekuyvnx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdra2xram9hdHZieGZla3V5dm54Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzM2MDMxOCwiZXhwIjoyMDc4OTM2MzE4fQ.YourServiceRoleKey"  # 서비스 롤 키 필요

# CSV 파일 경로
CSV_FILE_PATH = "서울시_생활인구_2023.csv"

def upload_csv_to_supabase():
    """CSV 파일을 읽어서 Supabase에 업로드"""
    # Supabase 클라이언트 초기화 (서비스 롤 키 필요)
    # 참고: 서비스 롤 키는 Supabase 대시보드의 Settings > API에서 확인 가능
    # 보안을 위해 환경 변수로 관리하는 것을 권장합니다
    
    print("CSV 파일 읽기 중...")
    
    # CSV 파일 읽기
    if not os.path.exists(CSV_FILE_PATH):
        print(f"오류: {CSV_FILE_PATH} 파일을 찾을 수 없습니다.")
        return
    
    data_to_insert = []
    batch_size = 1000  # 배치 크기
    
    with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            # CSV 컬럼명을 테이블 컬럼명에 맞게 변환
            data_to_insert.append({
                'date': row['날짜'],
                'time_hour': int(row['시간대']),
                'district_code': int(row['행정동코드']),
                'total_population': float(row['총생활인구수'])
            })
            
            # 배치 단위로 업로드
            if len(data_to_insert) >= batch_size:
                upload_batch(data_to_insert)
                data_to_insert = []
                print(f"업로드 중... ({len(data_to_insert)}개 행)")
        
        # 남은 데이터 업로드
        if data_to_insert:
            upload_batch(data_to_insert)
    
    print("업로드 완료!")

def upload_batch(data):
    """배치 데이터를 Supabase에 업로드"""
    # 주의: 이 함수를 사용하려면 서비스 롤 키가 필요합니다
    # 또는 Supabase 대시보드에서 CSV import 기능을 사용하세요
    print(f"배치 업로드: {len(data)}개 행")
    # 실제 업로드 로직은 서비스 롤 키가 필요하므로
    # Supabase 대시보드의 Table Editor > Insert > Import Data from CSV를 사용하는 것을 권장합니다

if __name__ == "__main__":
    print("=" * 50)
    print("CSV 파일을 Supabase에 업로드합니다.")
    print("=" * 50)
    print("\n주의: 이 스크립트를 사용하려면 서비스 롤 키가 필요합니다.")
    print("대신 Supabase 대시보드에서 CSV import 기능을 사용하는 것을 권장합니다:")
    print("1. Supabase 대시보드 접속")
    print("2. Table Editor > seoul_population 테이블 선택")
    print("3. Insert > Import Data from CSV 클릭")
    print("4. 서울시_생활인구_2023.csv 파일 업로드")
    print("=" * 50)
    
    # upload_csv_to_supabase()  # 서비스 롤 키 설정 후 주석 해제

