"""
CSV 파일의 한글 헤더를 영어로 변환하는 스크립트
사용법: python convert_csv_headers.py
"""
import csv
import os

# 입력 및 출력 파일 경로
INPUT_CSV = "서울시_생활인구_2023.csv"
OUTPUT_CSV = "서울시_생활인구_2023_english_headers.csv"

# 컬럼명 매핑 (한글 → 영어)
COLUMN_MAPPING = {
    '날짜': 'date',
    '시간대': 'time_hour',
    '행정동코드': 'district_code',
    '총생활인구수': 'total_population'
}

def convert_csv_headers():
    """CSV 파일의 헤더를 한글에서 영어로 변환"""
    
    if not os.path.exists(INPUT_CSV):
        print(f"오류: {INPUT_CSV} 파일을 찾을 수 없습니다.")
        return
    
    print(f"CSV 파일 변환 중: {INPUT_CSV} → {OUTPUT_CSV}")
    
    with open(INPUT_CSV, 'r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)
        
        # 원본 헤더 확인 (BOM 제거)
        original_headers = reader.fieldnames
        if original_headers:
            # BOM 제거
            original_headers = [header.strip('\ufeff') if header.startswith('\ufeff') else header for header in original_headers]
            reader.fieldnames = original_headers
        
        print(f"\n원본 헤더: {original_headers}")
        
        # 필요한 컬럼만 선택 (우리가 사용하는 컬럼만)
        required_columns = ['날짜', '시간대', '행정동코드', '총생활인구수']
        english_headers = [COLUMN_MAPPING[col] for col in required_columns]
        
        print(f"변환된 헤더: {english_headers}")
        
        # 새 CSV 파일 작성
        with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=english_headers)
            writer.writeheader()
            
            row_count = 0
            skipped_count = 0
            
            for row in reader:
                # BOM이 포함된 키 처리
                date_key = '날짜'
                if '\ufeff날짜' in row:
                    date_key = '\ufeff날짜'
                
                # 필요한 컬럼만 추출하여 변환
                date_value = row.get(date_key, row.get('날짜', '')).strip()
                time_hour_value = row.get('시간대', '').strip()
                district_code_value = row.get('행정동코드', '').strip()
                total_population_value = row.get('총생활인구수', '').strip()
                
                # 결측치 확인 (빈 값, None, 또는 공백만 있는 경우)
                if not date_value or not time_hour_value or not district_code_value or not total_population_value:
                    skipped_count += 1
                    continue
                
                # 숫자 필드 유효성 검사
                try:
                    int(time_hour_value)
                    int(district_code_value)
                    float(total_population_value)
                except (ValueError, TypeError):
                    skipped_count += 1
                    continue
                
                # 결측치가 없는 행만 작성
                new_row = {
                    'date': date_value,
                    'time_hour': time_hour_value,
                    'district_code': district_code_value,
                    'total_population': total_population_value
                }
                writer.writerow(new_row)
                row_count += 1
                
                # 진행 상황 출력 (1000행마다)
                if row_count % 1000 == 0:
                    print(f"처리 중... {row_count}개 행 (건너뛴 행: {skipped_count}개)")
    
    print(f"\n변환 완료!")
    print(f"- 저장된 행: {row_count}개")
    print(f"- 제거된 행 (결측치 포함): {skipped_count}개")
    print(f"- 총 처리된 행: {row_count + skipped_count}개")
    print(f"\n{OUTPUT_CSV} 파일에 저장되었습니다.")
    print(f"\n다음 단계:")
    print(f"1. Supabase 대시보드 접속")
    print(f"2. Table Editor > seoul_population 테이블 선택")
    print(f"3. Insert > Import Data from CSV 클릭")
    print(f"4. {OUTPUT_CSV} 파일 업로드")

if __name__ == "__main__":
    print("=" * 60)
    print("CSV 파일 헤더 변환 스크립트")
    print("=" * 60)
    convert_csv_headers()
    print("=" * 60)

